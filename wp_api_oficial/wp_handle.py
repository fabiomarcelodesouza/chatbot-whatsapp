# Importando bibliotecas necessárias
import os
from flask import jsonify
import wp_text
import wp_audio
import wp_openai

# Função para lidar com mensagens recebidas via webhook
def handle_message(request):
    # Analisar o corpo da requisição no formato json
    body = request.get_json()
    print(f"corpo da requisição: {body}")

    try:
        # Informações sobre o payload de mensagem de texto no WhatsApp:
        # https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples#text-messages   
        if body.get8("object"):
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

# Função para lidar com mensagens do WhatsApp de diferentes tipos
def handle_whatsapp_message(body):
    # Obter a mensagem do corpo da requisição
    message = body["entry"][0]["changes"][0]["value"]["messages"][0]

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