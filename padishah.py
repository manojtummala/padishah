from flask import Flask, redirect, render_template, request
from signal import signal, SIGTERM, SIGINT, SIGKILL
import subprocess
import threading
import time

""" global variables """
wait_list = []
is_running = False
picket_item = []
profile_list = []
processed = 0
total = 10
""" global variables """

app = Flask(__name__)
@app.route("/")
def home():
    if is_running:
        wait_list[0][2] = "{}/{}".format(processed, total)
    return render_template('index.html', display_list=wait_list, profiles=profile_list)

@app.route('/add-queue-item',methods=["GET","POST"])
def add_queue_item():
    if request.method == 'POST':
        folder = request.form.get("fname")
        profile = request.form.get("profile")
        cron_thread_lock.acquire()
        wait_list.append([folder, profile, "waiting"])
        cron_thread_lock.release()
    return redirect("/")

def cron_pickup():
    global is_running
    global wait_list
    global picket_item
    global processed
    while True:
        if not is_running and len(wait_list)>0:
            print("cron: picked up")
            processed = 0
            is_running = True
            for i in range(total):
                print("cron: processed {}".format(processed))
                time.sleep(5)
                processed += 1
            if wait_list[0][2] != "failed":
                print("cron: moving files to main dir")
            else:
                print("cron: keeping the incomplete files as they are")
            cron_thread_lock.acquire()
            wait_list.pop(0)
            cron_thread_lock.release()
            is_running = False
            print("cron: pick complete")

def cleanup(signal, frame):
    print("doing cleanup")
    if is_running:
        print("cleaning up incomplete encode")
    exit(0)

signal(SIGTERM, cleanup)
signal(SIGINT, cleanup)

cron_thread = threading.Thread(target=cron_pickup, daemon=True)
cron_thread.start()
cron_thread_lock = threading.Lock()

# load any queue items from persisting storage

# load profiles
profile_list = ["anime720p", "anime1080p"]

if __name__ == '__main__':
    app.run()
