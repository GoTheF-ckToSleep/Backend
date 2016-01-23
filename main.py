from apscheduler.scheduler import Scheduler
from datetime import datetime, timedelta, date
from flask import Flask, g, request
import json
import time
from TwitterAPI import TwitterAPI
from twilio.rest import TwilioRestClient
secret = open("secret").read().strip()
access_secret = open("access_secret").read().strip()
twilio_sid = open("twilio_sid").read().strip()
twilio_token = open("twilio_token").read().strip()
twilio_from = "+12892361862"
app = Flask(__name__)
base_url = "/api/"
ignore_urls = [base_url, "/static/<path:filename>"]
sched = Scheduler()
sched.start()

# twitter api
api = TwitterAPI('fmLOenZcTt4YQcgyaiTk6ILne', secret,
        '396757952-pYmsJGekmXKioPFUVOsjQtjpxQZxGc2z012LeFRA', access_secret)

# twilio api
smsapi = TwilioRestClient(twilio_sid, twilio_token)


def wakeup():
    global twitter
    global twilio
    if (twitter):
        r = api.request('statuses/update', {'status': "Good Morning!"})
    if (twilio):
        smsapi.messages.create(body="Good Morning!",
            to=twilio,
            from_=twilio_from)
    # Put the code here to wake someone up
    pass

def sleep():
    global twitter
    global twilio
    if (twitter):
        r = api.request('statuses/update', {'status': "Good night!"})
    if (twilio):
        smsapi.messages.create(body="Go to bed!",
            to=twilio,
            from_=twilio_from)
    # Put the code here to remind someone to sleep
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
            self.alarm_sleep.remove()
        if ("wakeup" in self.alarms):
            self.alarm_wakeup.remove()
        if self.sleep > datetime.now():
            self.alarm_sleep = sched.add_date_job(sleep, self.sleep, [])
        self.alarm_wakeup = sched.add_date_job(wakeup, self.wakeup, [])

    def __str__(self):
        return json.dumps({
            "sleep" : self.sleep.strftime(self.time_format),
            "wakeup" : self.wakeup.strftime(self.time_format),
        })

alarm = Alarm("%H:%M")
twitter = False
twilio = False

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

@app.route(base_url + "twitter", methods=["GET", "POST", "PUT"])
def toggle_twitter():
    global twitter
    if request.method == "GET":
        return json.dumps({"twitter" : twitter})
    else:
        twitter = not twitter
        return json.dumps({"twitter" : twitter})

@app.route(base_url + "twilio", methods=["GET", "POST", "PUT"])
def toggle_twilio():
    global twilio
    if request.method == "GET":
        return json.dumps({"twilio" : twilio})
    else:
        twilio = request.data.decode('utf-8')
        return json.dumps({"twilio" : twilio})

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
