import random
import requests
from controllers.MessageLogController import MessageLogController
from controllers.APIController import APIController
from controllers.OpenAIController import OpenAIController
from models.DatabaseModel import DatabaseModel
from utils.Enums.StatusAtendimento import StatusAtendimento
from models.ConversationModel import ConversationModel

class AtendimentoPorTextoController:
    def __init__(self):
        pass

    def inicia_atendimento(self, conversation_model, log_mensagens):
        message_log_controler = MessageLogController()
        database_model = DatabaseModel()

        conversation_model.nome_cliente, status = database_model.identifica_cliente(conversation_model.phone_number)
        conversation_model.status_atendimento = StatusAtendimento.ClienteIdentificado if status == 200 else StatusAtendimento.ClienteNaoIdentificado

        self.processa_mensagens(conversation_model, log_mensagens)

    def processa_mensagens(self, conversation_model, log_mensagens):
        message_log_controler = MessageLogController()
        database_model = DatabaseModel()

        if conversation_model.status_atendimento in {StatusAtendimento.ClienteIdentificado, StatusAtendimento.ClienteNaoIdentificado}:          
            lista_mensagens = database_model.obtem_mensagens(status_atendimento=conversation_model.status_atendimento)[0]
            mensagem = random.choice(lista_mensagens)[0].replace("[nome_cliente]", conversation_model.nome_cliente)      

            conversation_model.resposta = mensagem
            
            message_log_controler.update_message_log(conversation_model, log_mensagens)

            self.envia_mensagem_whatsapp(conversation_model.phone_number, mensagem)

        
    def confirmando_cadastro(self, conversation, phone_number, log_mensagens):
        message_log_controler = MessageLogController()
        database_model = DatabaseModel()

        nome_cliente = conversation
        status_atendimento = StatusAtendimento.ConfirmandoCadastro

        message_log_controler.update_message_log(message=conversation, phone_number=phone_number, role="user", status_atendimento=status_atendimento.name, nome_cliente=nome_cliente, log_mensagens=log_mensagens)
        
        lista_mensagens = database_model.obtem_mensagens(status_atendimento=status_atendimento)[0]
        mensagem = random.choice(lista_mensagens)[0].replace("[nome_cliente]", conversation)      
              
        message_log_controler.update_message_log(message=mensagem, phone_number=phone_number, role="assistant", status_atendimento=status_atendimento.name, nome_cliente=conversation, log_mensagens=log_mensagens)

        self.envia_mensagem_whatsapp(phone_number, mensagem)

    def cadastro_confirmado(self, conversation, phone_number, log_mensagens):
        message_log_controler = MessageLogController()
        database_model = DatabaseModel()

        nome_cliente = log_mensagens[phone_number]['nome_cliente']
        status_atendimento = StatusAtendimento.CadastroConfirmado.name
 
        message_log_controler.update_message_log(message=conversation, phone_number=phone_number, role="user", status_atendimento=status_atendimento, nome_cliente=nome_cliente, log_mensagens=log_mensagens)
       
        database_model.cadastrar_cliente(nome_cliente, phone_number)
        mensagem = f"Perfeito {nome_cliente}, agora que já nos conhecemos, em que posso te ajudar?"

        message_log_controler.update_message_log(message=mensagem, phone_number=phone_number, role="assistant", status_atendimento=status_atendimento, nome_cliente=nome_cliente, log_mensagens=log_mensagens)

        self.envia_mensagem_whatsapp(phone_number, mensagem)

    def cadastro_nao_confirmado(self, conversation, phone_number, log_mensagens):
        message_log_controler = MessageLogController()
        database_model = DatabaseModel()

        status_atendimento = StatusAtendimento.CadastroNaoConfirmado

        message_log_controler.update_message_log(message=conversation, phone_number=phone_number, role="user", status_atendimento=status_atendimento.name, nome_cliente=log_mensagens[phone_number]['nome_cliente'], log_mensagens=log_mensagens)

        lista_mensagens = database_model.obtem_mensagens(status_atendimento)[0]
        mensagem = random.choice(lista_mensagens)[0]   

        status_atendimento = StatusAtendimento.ClienteNaoIdentificado

        message_log_controler.update_message_log(message=mensagem, phone_number=phone_number, role="assistant", status_atendimento=status_atendimento.name, nome_cliente=log_mensagens[phone_number]['nome_cliente'], log_mensagens=log_mensagens)

        self.envia_mensagem_whatsapp(phone_number, mensagem)

    def opcao_confirmacao_invalida(self, conversation, phone_number, log_mensagens):
        message_log_controler = MessageLogController()
        database_model = DatabaseModel()

        status_atendimento = StatusAtendimento.DadosConfirmacaoInvalidos

        message_log_controler.update_message_log(message=conversation, phone_number=phone_number, role="user", status_atendimento=status_atendimento.name, nome_cliente=log_mensagens[phone_number]['nome_cliente'], log_mensagens=log_mensagens)

        lista_mensagens = database_model.obtem_mensagens(status_atendimento)[0]
        mensagem = random.choice(lista_mensagens)[0]   

        message_log_controler.update_message_log(message=mensagem, phone_number=phone_number, role="assistant", status_atendimento=status_atendimento.name, nome_cliente=log_mensagens[phone_number]['nome_cliente'], log_mensagens=log_mensagens)

        self.envia_mensagem_whatsapp(phone_number, mensagem)

    def cliente_identificado(self, conversation, phone_number, log_mensagens):
        open_ai_controller = OpenAIController()
        message_log_controler = MessageLogController()

        status_atendimento = StatusAtendimento.ClienteIdentificado

        message_log_controler.update_message_log(message=conversation, phone_number=phone_number, role="user", status_atendimento=status_atendimento.name, nome_cliente=log_mensagens[phone_number]['nome_cliente'], log_mensagens=log_mensagens)

        mensagem = open_ai_controller.make_openai_request(conversation, phone_number, log_mensagens)

        message_log_controler.update_message_log(message=mensagem, phone_number=phone_number, role="assistant", status_atendimento=status_atendimento.name, nome_cliente=log_mensagens[phone_number]['nome_cliente'], log_mensagens=log_mensagens)

        self.envia_mensagem_whatsapp(phone_number, mensagem)

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