# Importando bibliotecas necessárias
import os
import random
from flask import jsonify
#import controller_json as c_json
#import controller_json as c_json

from model import database as database

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
       # conversation, phone_number = c_json.handle_received_json(body)
        phone_number = phone_number.replace('@s.whatsapp.net', '')
        nome_cliente, status = database.identifica_cliente(phone_number)        
        cliente_identificado = status == 200 

        #c_json.update_message_log("jj", phone_number, "role", message_log_dict)

        
        print(f'Dicionario de log de mensagens: {message_log_dict}')

        lista_saudacoes = database.obtem_mensagens_saudacao(cliente_identificado=cliente_identificado)[0]
        saudacao = random.choice(lista_saudacoes)[0].replace("[nome_cliente]", nome_cliente)            
        
        #c_text.send_whatsapp_message(body, saudacao)

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
    

