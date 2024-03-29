# Importando bibliotecas necessárias
from dotenv import load_dotenv
load_dotenv()
import os
import requests

# Obtendo o token do WhatsApp a partir das variáveis de ambiente
whatsapp_token = os.environ["API_KEY_WHATSAPP"]
API_ADDRESS = os.environ["API_ADDRESS"]
INSTANCE = os.environ["INSTANCE"]

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
    from_number = body["data"]["key"]["remoteJid"] 
    url = f"{API_ADDRESS}/message/sendText/{INSTANCE}"
    print(url)

    # Definindo os cabeçalhos para autenticação e tipo de conteúdo
    headers = {
        'Content-Type': 'application/json',
        'apikey': 'zYzP7ocstxh3SJ23D4FZTCu4ehnM8v4hu',
        'Cookie': 'codechat.api.sid=s%3AGSt-cXivcvVlfRTr03XfrBQyC8ujMkbh.DiSkxCfvBhaEwP48Z7XYG%2BZ%2ByD7gCUTXHxIbcPGREPE'
    }

    # Criando os dados da mensagem com informações como tipo, destinatário e corpo da mensagem
    data = {
        "number": from_number,
        "options": {
            "delay": 0,
            "presence": "composing"
        },
        "textMessage": {
            "text": message
        }
    }

    return url, headers, data