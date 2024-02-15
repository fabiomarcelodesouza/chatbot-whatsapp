from controllers.VariaveisAmbienteController import VariaveisAmbienteController

class APIController:
    def __init__(self):
        pass

    def build_api_call(self, phone_number, message):
        variaveis_ambiente = VariaveisAmbienteController()

        # Obtendo informações relevantes da requisição recebida
        url = f"{variaveis_ambiente.API_ADDRESS}/message/sendText/{variaveis_ambiente.INSTANCE}"
        print(url)

        # Definindo os cabeçalhos para autenticação e tipo de conteúdo
        headers = {
            'Content-Type': 'application/json',
            'apikey': 'zYzP7ocstxh3SJ23D4FZTCu4ehnM8v4hu',
            'Cookie': 'codechat.api.sid=s%3AGSt-cXivcvVlfRTr03XfrBQyC8ujMkbh.DiSkxCfvBhaEwP48Z7XYG%2BZ%2ByD7gCUTXHxIbcPGREPE'
        }

        # Criando os dados da mensagem com informações como tipo, destinatário e corpo da mensagem
        data = {
            "number": phone_number,
            "options": {
                "delay": 0,
                "presence": "composing"
            },
            "textMessage": {
                "text": message
            }
        }

        return url, headers, data