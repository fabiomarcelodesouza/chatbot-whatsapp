import os
from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()
import controller.controller_tools as c_tools
import controller.controller_handle2 as c_handle
import controller.abobora as abobora

print(abobora.vairtomarnocu())
app = Flask(__name__)

# Sets homepage endpoint and welcome message
@app.route("/", methods=["GET"])
def home():
    return "WhatsApp OpenAI Webhook is listening!"

# Accepts POST and GET requests at /webhook endpoint
@app.route("/webhook", methods=["POST", "GET"]) 
def webhook(): 
    if request.method == "GET":
        return c_tools.verify_webhook(request)
    elif request.method == "POST":
        return c_handle.handle_message(request)
 
# Route to reset message log
@app.route("/reset", methods=["GET"])
def reset():
    global message_log_dict
    message_log_dict = {}
    return "Message log resetted!"

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=5000)