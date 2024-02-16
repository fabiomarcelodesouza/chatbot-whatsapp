import datetime
from flask import Flask, request
from controllers.WebhookController import WebhookController
from controllers.RecebimentoMensagemController import RecebimentoMensagemController
from controllers.LoggingController import LoggingController
import logging

app = Flask(__name__)
log_mensagens = {}

data_hora_atual = datetime.datetime.now()
nome_arquivo = "./log/" + data_hora_atual.strftime("%Y-%m-%d_%H-%M-%S") + ".log"
logging.basicConfig(filename=nome_arquivo, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Sets homepage endpoint and welcome message
@app.route("/", methods=["GET"])
def home():
    return "WhatsApp OpenAI Webhook is listening!"

# Accepts POST and GET requests at /webhook endpoint
@app.route("/webhook", methods=["POST", "GET"]) 
def webhook():    
    try:
        if request.method == "GET":
            webhook_controller = WebhookController()
            return webhook_controller.verify_webhook(request)
        elif request.method == "POST":
            recebe_mensagem_controller = RecebimentoMensagemController()
            return recebe_mensagem_controller.recebe_mensagem(request, log_mensagens)
    except Exception as error:
        LoggingController.registrar_log(logger.error, error)
 
# Route to reset message log
@app.route("/reset", methods=["GET"])
def reset():
    global log_mensagens
    log_mensagens = {}
    return "Message log resetted!"

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=5000)