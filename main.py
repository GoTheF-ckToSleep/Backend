from flask import Flask
import json
app = Flask(__name__)
ignore_urls = ["/api", "/static/<path:filename>"]

@app.route("/api")
def list_urls():
    urls = [rule.rule for rule in app.url_map.iter_rules() 
            if (rule.rule not in ignore_urls)]
    return json.dumps(urls)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
