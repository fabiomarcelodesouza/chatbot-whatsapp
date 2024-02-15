from flask import jsonify
from controllers.VariaveisAmbienteController import VariaveisAmbienteController

class WebhookController:
    def __init__(self):
        pass
            
    # Função para verificar o webhook de acordo com as informações da solicitação
    def verify_webhook(self, request):
        # Analisando parâmetros da solicitação de verificação do webhook
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        # Verificando se um modo e token foram enviados
        if mode and token:
            variaveis_ambiente = VariaveisAmbienteController()

            # Verificando se o modo e token enviados estão corretos
            if mode == "subscribe" and token == variaveis_ambiente.VERIFY_TOKEN:
                # Respondendo com 200 OK e o token de desafio da solicitação
                print("WEBHOOK_VERIFIED")
                return challenge, 200
            else:
                # Responde com '403 Forbidden' se os tokens de verificação não corresponderem
                print("VERIFICATION_FAILED")
                return jsonify({"status": "error", "message": "Verificação falhou"}), 403
        else:
            # Responde com '400 Bad Request' se os tokens de verificação não corresponderem
            print("MISSING_PARAMETER")
            return jsonify({"status": "error", "message": "Parâmetros ausentes"}), 400