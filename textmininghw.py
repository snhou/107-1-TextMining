import urllib
import json
import os
from flask import Flask
from flask import request
from flask import make_response
app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "askweather":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("weatherlocation")
    cost = {'Taipei':'18', 'Kaohsiung':'20', 'Taichung':'10','Tainan':'25'}
    speech = "The temperatrue of " + zone + " is " + str(cost[zone])
    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        "source": "agent"
    }

if __name__ == "__main__":
    app.run(debug=True,port=80)