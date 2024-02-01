# Importando bibliotecas necessárias
from dotenv import load_dotenv
load_dotenv()
import os
import requests

# Obtendo o token do WhatsApp a partir das variáveis de ambiente
whatsapp_token = os.environ["API_KEY_WHATSAPP"]

# Função para enviar a resposta como uma mensagem no WhatsApp de volta para o usuário
def send_whatsapp_message(body, message):
    # Obtendo informações relevantes da requisição recebida
    
    url, headers, data = build_api_call(body, message)

    # Enviando a mensagem usando o método POST e os cabeçalhos definidos
    response = requests.post(url, json=data, headers=headers)
    
    print(f"Resposta da mensagem no WhatsApp: {response.json()}")
    # Verificando se houve algum erro na resposta
    response.raise_for_status()
 
#Função para identificar se está sendo utilizada a API oficial do WhatsApp ou a da PrimeVirtu e montar a requisição de acordo com cada uma
def build_api_call(body, message):
    # Obtendo informações relevantes da requisição recebida    
    value = body["entry"][0]["changes"][0]["value"]
    phone_number_id = value["metadata"]["phone_number_id"]
    from_number = value["messages"][0]["from"]   

    url = "https://graph.facebook.com/v15.0/" + phone_number_id + "/messages"

    # Definindo os cabeçalhos para autenticação e tipo de conteúdo
    headers = {
        "Authorization": f"Bearer {whatsapp_token}",
        "Content-Type": "application/json",
    }

    # Criando os dados da mensagem com informações como tipo, destinatário e corpo da mensagem
    data = {
        "messaging_product": "whatsapp",
        "to": from_number,
        "type": "text",
        "text": {"body": message},
    }
   
    return url, headers, data