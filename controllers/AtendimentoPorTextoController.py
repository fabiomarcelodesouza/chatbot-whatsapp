import random
import requests
from controllers.MessageLogController import MessageLogController
from controllers.APIController import APIController
from models.DatabaseModel import DatabaseModel

class AtendimentoPorTextoController:
    def __init__(self):
        pass

    # Função para enviar a resposta como uma mensagem no WhatsApp de volta para o usuário
    def envia_mensagem_whatsapp(self, phone_number, message):
        # Obtendo informações relevantes da requisição recebida
        api_controller = APIController()
        url, headers, data = api_controller.build_api_call(phone_number, message)

        # Enviando a mensagem usando o método POST e os cabeçalhos definidos
        response = requests.post(url, json=data, headers=headers)
        
        print(f"Resposta da mensagem no WhatsApp: {response.json()}")

        # Verificando se houve algum erro na resposta
        response.raise_for_status()

    def inicia_atendimento(self, conversation, phone_number, log_mensagens):
        message_log_controler = MessageLogController()
        database_model = DatabaseModel()

        nome_cliente, status = database_model.identifica_cliente(phone_number)        
        cliente_identificado = status == 200 

        chat_status = "iniciado"

        message_log_controler.update_message_log(message=conversation, phone_number=phone_number, role="user", chat_status=chat_status, nome_cliente=nome_cliente, log_mensagens=log_mensagens)
        
        lista_mensagens = database_model.obtem_mensagens_saudacao(cliente_identificado=cliente_identificado)[0]
        mensagem = random.choice(lista_mensagens)[0].replace("[nome_cliente]", nome_cliente)      
              
        message_log_controler.update_message_log(message=mensagem, phone_number=phone_number, role="assistant", chat_status=chat_status, nome_cliente=nome_cliente, log_mensagens=log_mensagens)

        self.envia_mensagem_whatsapp(phone_number, mensagem)

    def confirma_cadastro(self, conversation, phone_number, log_mensagens):
        message_log_controler = MessageLogController()
        database_model = DatabaseModel()

        nome_cliente = conversation
        chat_status = "confirmando_cadastro"

        message_log_controler.update_message_log(message=conversation, phone_number=phone_number, role="user", chat_status=chat_status, nome_cliente=nome_cliente, log_mensagens=log_mensagens)
        
        lista_mensagens = database_model.obtem_mensagens_confirmacao_cadastro()[0]
        mensagem = random.choice(lista_mensagens)[0].replace("[nome_cliente]", conversation)      
              
        message_log_controler.update_message_log(message=mensagem, phone_number=phone_number, role="assistant", chat_status=chat_status, nome_cliente=conversation, log_mensagens=log_mensagens)

        self.envia_mensagem_whatsapp(phone_number, mensagem)

    def cadastra_usario(self, body, conversation, phone_number, log_mensagens, status_cadastro):
        message_log_controler = MessageLogController()
        database_model = DatabaseModel()

        print(f'statuuuuuuuuuuuuuuuuuuuuuuuuus    {status_cadastro}')
        if status_cadastro == 'iniciando_cadastro':
            message_log_controler.update_message_log(message=conversation, phone_number=phone_number, role="user", chat_status="iniciado", nome_cliente="", log_mensagens=log_mensagens)
            status_cadastro = 'confirmando_cadastro'
            lista_mensagens = database_model.obtem_mensagens_confirmacao_cadastro()[0]
            mensagem = random.choice(lista_mensagens)[0].replace("[nome_cliente]", conversation)            
            message_log_controler.update_message_log(message=mensagem, phone_number=phone_number, role="assistant", chat_status=status_cadastro, nome_cliente=conversation, log_mensagens=log_mensagens)
        
        elif status_cadastro == 'confirmando_cadastro':
            message_log_controler.update_message_log(message=conversation, phone_number=phone_number, role="user", chat_status=status_cadastro, nome_cliente=conversation, log_mensagens=log_mensagens)
            print(f'lá eleeeeeeeeeeeee     {conversation}')
            if (conversation == '1' or 
                'sim' in conversation.lower()):
                status_cadastro = 'cadastro_confirmado'
                database_model.cadastrar_cliente(log_mensagens[phone_number]["nome_cliente"], phone_number)
                mensagem = f"Perfeito {log_mensagens[phone_number]['nome_cliente']}, agora que já nos conhecemos, em que posso te ajudar?"
                message_log_controler.update_message_log(message=mensagem, phone_number=phone_number, role="assistant", chat_status=status_cadastro, nome_cliente=log_mensagens[phone_number]['nome_cliente'], log_mensagens=log_mensagens)
        
            if (conversation == '2' or 
                'não' in conversation.lower() or 
                'nao' in conversation.lower()):
                status_cadastro = 'cadastro_nao_confirmado'
                mensagem = f"Sem problemas, vamos tentar de novo, me informe o seu nome comleto! Digite no campo abaixo somente o seu nome completo, ok? Pode digitar."
                message_log_controler.update_message_log(message=mensagem, phone_number=phone_number, role="assistant", chat_status=status_cadastro, nome_cliente=log_mensagens[phone_number]['nome_cliente'], log_mensagens=log_mensagens)

        self.envia_mensagem_whatsapp(body, mensagem)