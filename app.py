import os
from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()
import wp_common.wp_tools as wp_tools
API_OFICIAL = os.environ["USE_OFICIAL_API"]
if API_OFICIAL == True:
    import wp_api_oficial.wp_handle as wp_handle
else:
    import wp_api_codechat.wp_handle as wp_handle

app = Flask(__name__)

# Sets homepage endpoint and welcome message
@app.route("/", methods=["GET"])
def home():
    return "WhatsApp OpenAI Webhook is listening!"

# Accepts POST and GET requests at /webhook endpoint
@app.route("/webhook", methods=["POST", "GET"]) 
def webhook(): 
    if request.method == "GET":
        return wp_tools.verify_webhook(request)
    elif request.method == "POST":
        return wp_handle.handle_message(request)
 
# Route to reset message log
@app.route("/reset", methods=["GET"])
def reset():
    global message_log_dict
    message_log_dict = {}
    return "Message log resetted!"

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=5000)