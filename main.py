from flask import Flask, g, request
import json
from time import strptime, strftime
app = Flask(__name__)
base_url = "/api/"
ignore_urls = [base_url, "/static/<path:filename>"]

class Alarm():
    def __init__(self, time_format):
        self.time = None
        self.time_format = time_format

    def set_alarm(self, time):
        strtime = time.decode("utf-8")
        self.time = strptime(strtime, self.time_format)

    def __str__(self):
        return strftime(self.time_format, self.time)

alarm = Alarm("%H:%M")

@app.route(base_url)
def list_urls():
    urls = [rule.rule for rule in app.url_map.iter_rules() 
            if (rule.rule not in ignore_urls)]
    return json.dumps(urls)

@app.route(base_url + "toggle")
def toggle_switch():
    return "this endpoint will eventuall toggle the light on/off"

@app.route(base_url + "alarm", methods=["GET", "POST", "PUT"])
def set_alarm():
    if request.method == "GET":
        return alarm.time
    else:
        alarm.set_alarm(request.data)
        return "Alarm set for %s" % alarm

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
