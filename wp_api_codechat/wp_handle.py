# Importando bibliotecas necessárias
import os
from flask import jsonify
import wp_api_codechat.wp_text as wp_text
import wp_common.wp_audio as wp_audio
import wp_common.wp_openai as wp_openai

# Função para lidar com mensagens recebidas via webhook
def handle_message(request):
    # Analisar o corpo da requisição no formato json
    body = request.get_json()
    print(f"corpo da requisição: {body}")

    try:
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

# Função para lidar com mensagens do WhatsApp de diferentes tipos
def handle_whatsapp_message(body):
    # Obter a mensagem do corpo da requisição
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