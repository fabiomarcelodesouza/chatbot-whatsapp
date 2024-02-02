# Importando bibliotecas necessárias
from dotenv import load_dotenv
load_dotenv()
import os
import requests
import controller_json as c_json

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