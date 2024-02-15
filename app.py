from flask import Flask, request
from controllers.WebhookController import WebhookController
from controllers.RecebimentoMensagemController import RecebimentoMensagemController

app = Flask(__name__)

log_mensagens = {}

# Sets homepage endpoint and welcome message
@app.route("/", methods=["GET"])
def home():
    return "WhatsApp OpenAI Webhook is listening!"

# Accepts POST and GET requests at /webhook endpoint
@app.route("/webhook", methods=["POST", "GET"]) 
def webhook():    
    if request.method == "GET":
        webhook_controller = WebhookController()
        return webhook_controller.verify_webhook(request)
    elif request.method == "POST":
        recebe_mensagem_controller = RecebimentoMensagemController()
        return recebe_mensagem_controller.recebe_mensagem(request, log_mensagens)
 
# Route to reset message log
@app.route("/reset", methods=["GET"])
def reset():
    global log_mensagens
    log_mensagens = {}
    return "Message log resetted!"

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=5000)