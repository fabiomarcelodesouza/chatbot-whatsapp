from flask import Flask, request
import wp_tools
import wp_handle

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