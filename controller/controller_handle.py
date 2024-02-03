# Importando bibliotecas necessárias
import json
import os
import random
from flask import jsonify
import controller.controller_json as c_json
import controller.controller_text as c_text
import model.database as database

# Dicionário de log de mensagens para permitir conversação ao longo de várias mensagens
message_log_dict = {}

# Função para lidar com mensagens recebidas via webhook
def handle_message(request):
    # Analisar o corpo da requisição no formato json
    body = request.get_json()
    
    try:
        if body.get("event") == "messages.upsert":
            if (
                body["data"]["message"]["conversation"]
            ):                
                handle_whatsapp_message(body)
            return jsonify({"status": "ok"}), 200
        else:
            # Se a requisição não for um evento da API do WhatsApp, retornar um erro
            return (
                jsonify({"status": "error", "message": "Evento não mapeado"}),
                204,
            )
    # Capturar todos os outros erros e retornar um erro interno do servidor
    except Exception as e:
        print(f"Erro desconhecido: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Função para lidar com mensagens do WhatsApp de diferentes tipos
def handle_whatsapp_message(body):
    # Obter a mensagem do corpo da requisição
    if body.get("event") == "messages.upsert":
        conversation, phone_number = c_json.handle_received_message(body)
        phone_number = phone_number.replace('@s.whatsapp.net', '')
        
        # Inicio de conversa              
        if phone_number not in message_log_dict:        
            c_text.inicia_atendimento(body, conversation, phone_number, message_log_dict)
        
        # Conversa inciada e usuario não identificado
        elif message_log_dict[phone_number]["status"] == "iniciado":
            c_text.cadastra_usario(body, conversation, phone_number, message_log_dict, "iniciando_cadastro")
            print(f'ABOBORAAAAAAAAAAAAAAA       {message_log_dict[phone_number]["status"]}')

        # Conversa inciada, usuario não identificado e esta em processo de confirmacao do cadastro
        elif (message_log_dict[phone_number]["status"] == "iniciando_cadastro" or
              message_log_dict[phone_number]["status"] == "confirmando_cadastro"):
            print(f'ABOBORAAAAAAAAAAAAAAA       {message_log_dict[phone_number]["status"]}')
            c_text.cadastra_usario(body, conversation, phone_number, message_log_dict, "confirmando_cadastro")        

        
        


       # if cliente_identificado:            




        # if body["data"]["message"]["conversation"]:
        #     message = {
        #         "text": {
        #             "body": body["data"]["message"]["conversation"]
        #         },
        #         "type": "text",
        #         "from": body["data"]["key"]["phone_number"]
        #     }
        # message_body = message["text"]["body"]
    # if message["type"] == "text":
    #     # Se a mensagem for do tipo texto, obter o corpo da mensagem
    #     message_body = message["text"]["body"]
    # elif message["type"] == "audio":
    #     # Se a mensagem for do tipo áudio, obter o ID do áudio e processar a mensagem de áudio
    #     audio_id = message["audio"]["id"]
    #     message_body = c_audio.handle_audio_message(audio_id)
    # # Fazer uma requisição ao OpenAI com o corpo da mensagem e o número do remetente
    # response = c_openai.make_openai_request(message_body, message["from"])
    # # Enviar a resposta via mensagem de texto no WhatsApp
    

