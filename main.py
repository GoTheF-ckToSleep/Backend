from apscheduler.scheduler import Scheduler
from datetime import datetime, timedelta, date
from flask import Flask, g, request
import json
import time
app = Flask(__name__)
base_url = "/api/"
ignore_urls = [base_url, "/static/<path:filename>"]
sched = Scheduler()
sched.start()

def wakeup():
    # Put the code here to wake someone up
    pass

def sleep():
    # Put the code here to remind someone to sleep
    print("go to sleep!")
    return

class Alarm():
    def __init__(self, time_format):
        self.sleep = None
        self.alarms = {}
        self.time_format = time_format

    def set_alarm(self, time):
        strtime = time.decode("utf-8")
        today = date.today()
        self.wakeup = datetime.strptime(strtime, self.time_format)
        self.wakeup = self.wakeup.replace(
            year = today.year,
            month = today.month,
            day = today.day)
        self.sleep = self.wakeup - timedelta(hours = 8)
        if self.wakeup < datetime.now():
            self.wakeup += timedelta(hours = 24)
            self.sleep = self.wakeup + timedelta(hours = 8)
        if ("sleep" in self.alarms):
            self.alarms.sleep.remove()
        if ("wakeup" in self.alarms):
            self.alarms.wakeup.remove()
        self.alarms = {
            "sleep" : sched.add_date_job(sleep, self.sleep, []),
            "wakeup" : sched.add_date_job(wakeup, self.wakeup, []),
        }

    def __str__(self):
        return json.dumps({
            "wakeup" : self.sleep.strftime(self.time_format),
            "sleep" : self.wakeup.strftime(self.time_format),
        })

alarm = Alarm("%H:%M")

@app.route(base_url)
def list_urls():
    urls = [rule.rule for rule in app.url_map.iter_rules() 
            if (rule.rule not in ignore_urls)]
    return json.dumps(urls)

@app.route(base_url + "toggle")
def toggle_switch():
    #exec('terrence put the toggle command here')
    return "this endpoint will eventuall toggle the light on/off"

@app.route(base_url + "alarm", methods=["GET", "POST", "PUT"])
def set_alarm():
    if request.method == "GET":
        return str(alarm)
    else:
        alarm.set_alarm(request.data)
        return str(alarm)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
