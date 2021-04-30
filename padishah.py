from flask import Flask, render_template
import scheduler as Scheduler
import threading
import time

app = Flask(__name__)
@app.route("/")
# show table with full waitlist or fist row running and waitlist
# show form with foldername (blank), profile (selector)
def home():
  return render_template('index.html')

@app.route("/about")
def about():
  return render_template("about.html")

# submit button in the home page form calls this
# post request json, folder name, profile name
@app.route('/add-queue-item')
def add_queue_item():
    Scheduler.add_waitlist_item()
    return

def cron_pickup():
    if not Scheduler.get_run_status():
        Scheduler.run_new_item()
    time.sleep(1000)

if __name__ == '__main__':
    Scheduler.init()
    flask_thread = threading.Thread('t1', target=app.run(debug = True))
    scheduler_thread = threading.Thread('t2', target=cron_pickup())
    flask_thread.start()
    scheduler_thread.start()
