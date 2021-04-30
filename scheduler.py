import threading
# queue to hold waitlist, take to element to run
waitlist_queue = None
# running status
is_running = None
picked_item = None
waitlist_queue_lock = None

def init():
    global waitlist_queue
    # running status
    global is_running
    global picked_item
    global waitlist_queue_lock

    waitlist_queue = []
    is_running = False
    picked_item = None
    waitlist_queue_lock = threading.lock()
    Encoder.init()

def get_run_status():
    return is_running

def get_waitlist_queue():
    return waitlist_queue

def add_waitlist_item(item):
    waitlist_queue_lock.acquire()
    waitlist_queue.append(item)
    waitlist_queue_lock.release()

def get_progress():
    return Encoder.get_processed() / Encoder.get_total()

def run_new_item():
    waitlist_queue_lock.acquire()
    picked_item = waitlist_queue[0]
    waitlist_queue = waitlist_queue[1:]
    waitlist_queue_lock.release()

    is_running = True
    return_code = Encoder.run(picked_item)

    # success, pick next when time comes
    if return_code == 0:
        is_running = False
    # failure, put it back to waitlist
    else:
        is_running = False
        waitlist_queue_lock.acquire()
        waitlist_queue.append(picked_item)
        waitlist_queue_lock.release()
        if return_code == 2:
            System.exit(0)
