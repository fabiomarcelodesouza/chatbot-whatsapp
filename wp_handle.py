# Importando bibliotecas necessárias
import os
from flask import jsonify
from dotenv import load_dotenv
load_dotenv()
import wp_text
import wp_audio
import wp_openai

USE_OFICIAL_API = os.environ["USE_OFICIAL_API"]

# Função para lidar com mensagens do WhatsApp de diferentes tipos
def handle_whatsapp_message(body):
    # Obter a mensagem do corpo da requisição
    if USE_OFICIAL_API == "True":
        message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    else:
        if body.get("event") == "messages.upsert":
            if body["data"]["message"]["conversation"]:
                message = {
                    "text": {
                        "body": body["data"]["message"]["conversation"]
                    },
                    "type": "text",
                    "from": body["data"]["key"]["remoteJid"]
                }

    if message["type"] == "text":
        # Se a mensagem for do tipo texto, obter o corpo da mensagem
        message_body = message["text"]["body"]
    elif message["type"] == "audio":
        # Se a mensagem for do tipo áudio, obter o ID do áudio e processar a mensagem de áudio
        audio_id = message["audio"]["id"]
        message_body = wp_audio.handle_audio_message(audio_id)
    # Fazer uma requisição ao OpenAI com o corpo da mensagem e o número do remetente
    response = wp_openai.make_openai_request(message_body, message["from"])
    # Enviar a resposta via mensagem de texto no WhatsApp
    wp_text.send_whatsapp_message(body, response)

# Função para lidar com mensagens recebidas via webhook
def handle_message(request):
    # Analisar o corpo da requisição no formato json
    body = request.get_json()
    print(f"corpo da requisição: {body}")

    try:
        # Informações sobre o payload de mensagem de texto no WhatsApp:
        # https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples#text-messages
        if USE_OFICIAL_API == "True":
            if body.get("object"):
                if (
                    body.get("entry")
                    and body["entry"][0].get("changes")
                    and body["entry"][0]["changes"][0].get("value")
                    and body["entry"][0]["changes"][0]["value"].get("messages")
                    and body["entry"][0]["changes"][0]["value"]["messages"][0]
                ):
                    # Se for um evento da API do WhatsApp, lidar com a mensagem do WhatsApp
                    handle_whatsapp_message(body)
                return jsonify({"status": "ok"}), 200
            # Lidando com retorno da API da PrimeVirtu
        else:
            if body.get("event") == "messages.upsert":
                print(body.get("instance"))
                if (
                    body["data"]["message"]["conversation"]
                ):
                    print(f"aaaaaaaaaaaaaaaaaaaaaa:")
                    handle_whatsapp_message(body)
                return jsonify({"status": "ok"}), 200
            else:
                # Se a requisição não for um evento da API do WhatsApp, retornar um erro
                return (
                    jsonify({"status": "error", "message": "Não é um evento da API do WhatsApp"}),
                    404,
                )
    # Capturar todos os outros erros e retornar um erro interno do servidor
    except Exception as e:
        print(f"Erro desconhecido: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
