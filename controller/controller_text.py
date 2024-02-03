# Importando bibliotecas necessárias
import random
from dotenv import load_dotenv
load_dotenv()
import os
import requests
import controller.controller_json as c_json
import model.database as database

# Obtendo o token do WhatsApp a partir das variáveis de ambiente
whatsapp_token = os.environ["API_KEY_WHATSAPP"]
API_ADDRESS = os.environ["API_ADDRESS"]
INSTANCE = os.environ["INSTANCE"]

# Função para enviar a resposta como uma mensagem no WhatsApp de volta para o usuário
def send_whatsapp_message(body, message):
    # Obtendo informações relevantes da requisição recebida
    
    url, headers, data = c_json.build_api_call(body, message, API_ADDRESS, INSTANCE)

    # Enviando a mensagem usando o método POST e os cabeçalhos definidos
    response = requests.post(url, json=data, headers=headers)
    
    print(f"Resposta da mensagem no WhatsApp: {response.json()}")
    # Verificando se houve algum erro na resposta
    response.raise_for_status()

def inicia_atendimento(body, conversation, phone_number, message_log_dict):
    nome_cliente, status = database.identifica_cliente(phone_number)        
    cliente_identificado = status == 200 

    c_json.update_message_log(message=conversation, phone_number=phone_number, role="user", chat_status="iniciado", nome_cliente=nome_cliente, message_log_dict=message_log_dict)
    lista_mensagens = database.obtem_mensagens_saudacao(cliente_identificado=cliente_identificado)[0]
    mensagem = random.choice(lista_mensagens)[0].replace("[nome_cliente]", nome_cliente)            
    c_json.update_message_log(message=mensagem, phone_number=phone_number, role="assistant", chat_status="iniciado", nome_cliente=nome_cliente, message_log_dict=message_log_dict)

    send_whatsapp_message(body, mensagem)

def cadastra_usario(body, conversation, phone_number, message_log_dict, status_cadastro):
    print(f'statuuuuuuuuuuuuuuuuuuuuuuuuus    {status_cadastro}')
    if status_cadastro == 'iniciando_cadastro':
        c_json.update_message_log(message=conversation, phone_number=phone_number, role="user", chat_status="iniciado", nome_cliente="", message_log_dict=message_log_dict)
        status_cadastro = 'confirmando_cadastro'
        lista_mensagens = database.obtem_mensagens_confirmacao_cadastro()[0]
        mensagem = random.choice(lista_mensagens)[0].replace("[nome_cliente]", conversation)            
        c_json.update_message_log(message=mensagem, phone_number=phone_number, role="assistant", chat_status=status_cadastro, nome_cliente=conversation, message_log_dict=message_log_dict)
    
    elif status_cadastro == 'confirmando_cadastro':
        c_json.update_message_log(message=conversation, phone_number=phone_number, role="user", chat_status=status_cadastro, nome_cliente=conversation, message_log_dict=message_log_dict)
        print(f'lá eleeeeeeeeeeeee     {conversation}')
        if (conversation == '1' or 
            'sim' in conversation.lower()):
            status_cadastro = 'cadastro_confirmado'
            database.cadastrar_cliente(message_log_dict[phone_number]["nome_cliente"], phone_number)
            mensagem = f"Perfeito {message_log_dict[phone_number]['nome_cliente']}, agora que já nos conhecemos, em que posso te ajudar?"
            c_json.update_message_log(message=mensagem, phone_number=phone_number, role="assistant", chat_status=status_cadastro, nome_cliente=message_log_dict[phone_number]['nome_cliente'], message_log_dict=message_log_dict)
    
        if (conversation == '2' or 
            'não' in conversation.lower() or 
            'nao' in conversation.lower()):
            status_cadastro = 'cadastro_nao_confirmado'
            mensagem = f"Sem problemas, vamos tentar de novo, me informe o seu nome comleto! Digite no campo abaixo somente o seu nome completo, ok? Pode digitar."
            c_json.update_message_log(message=mensagem, phone_number=phone_number, role="assistant", chat_status=status_cadastro, nome_cliente=message_log_dict[phone_number]['nome_cliente'], message_log_dict=message_log_dict)

    send_whatsapp_message(body, mensagem)