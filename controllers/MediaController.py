import requests
from controllers.VariaveisAmbienteController import VariaveisAmbienteController

class MediaController:
    # Dicionário de log de mensagens para permitir conversação ao longo de várias mensagens
    def __init__(self, headers):
        self._headers = headers

    @property
    def headers(self):
        variaveis_ambiente = VariaveisAmbienteController()
        
        headers = {
            "Authorization": f"Bearer {variaveis_ambiente.API_KEY_WHATSAPP}",
        }

        return headers
    
    # Obtendo a URL da mídia a partir do ID da mídia
    def get_media_url(self, media_id):
        url = f"https://graph.facebook.com/v16.0/{media_id}/"
        response = requests.get(url, headers=self.headers)
        return response.json()["url"]

    # Baixando o arquivo de mídia da URL da mídia
    def download_media_file(self, media_url):
        response = requests.get(media_url, headers=self.headers)
        return response.content
