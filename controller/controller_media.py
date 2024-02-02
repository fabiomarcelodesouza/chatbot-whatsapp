# Importando biblioteca necessária
from dotenv import load_dotenv
load_dotenv()
import os
import requests

# Obtendo o token do WhatsApp a partir das variáveis de ambiente
whatsapp_token = os.environ["API_KEY_WHATSAPP"]
headers = {
    "Authorization": f"Bearer {whatsapp_token}",
}

# Obtendo a URL da mídia a partir do ID da mídia
def get_media_url(media_id):
    url = f"https://graph.facebook.com/v16.0/{media_id}/"
    response = requests.get(url, headers=headers)
    return response.json()["url"]

# Baixando o arquivo de mídia da URL da mídia
def download_media_file(media_url):
    response = requests.get(media_url, headers=headers)
    return response.content
