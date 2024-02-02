#Função para identificar se está sendo utilizada a API oficial do WhatsApp ou a da PrimeVirtu e montar a requisição de acordo com cada uma
def build_api_call(body, message, API_ADDRESS, INSTANCE):
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

def handle_received_json(body):
    conversation = body["data"]["message"]["conversation"] if body["data"]["message"]["conversation"] else 404
    remoteJid = body["data"]["key"]["remoteJid"] if body["data"]["key"]["remoteJid"] else 404

    return conversation, remoteJid

# Função para criar ou atualizar o log de mensagens com a mensagem do usuário ou assistente
def update_message_log(message, phone_number, role, message_log_dict):
    # Log inicial com instruções e apresentação ao usuário
    initial_log = {"role": "system", "content": "Você é a Bela, assistente virtual do salão de beleza chamado Glowz Beauty Lounge",}    

    # Criar um novo log de mensagem com o papel (usuário ou assistente) e conteúdo da mensagem
    message_log = {"role": role, "content": message}
    # Adicionar o log de mensagem ao dicionário usando o número de telefone como chave
    if phone_number not in message_log_dict:
        message_log_dict[phone_number] = [initial_log]
    message_log_dict[phone_number].append(message_log)
    # Retornar o log de mensagens atualizado para o número de telefone
    return message_log_dict[phone_number]

