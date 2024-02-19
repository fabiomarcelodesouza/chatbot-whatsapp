import json
from controllers.VariaveisAmbienteController import VariaveisAmbienteController
from models.ConversationModel import ConversationModel

class MessageLogController:
    def __init__(self):
        pass

    # Função para criar ou atualizar o log de mensagens com a mensagem do usuário ou assistente
    def update_message_log(self, conversation_model, log_mensagens):
        self.update_message_log_user(conversation_model=conversation_model, log_mensagens=log_mensagens)
        self.update_message_log_assistant(conversation_model=conversation_model, log_mensagens=log_mensagens)
        return log_mensagens[conversation_model.phone_number]
    
    # Função para criar ou atualizar o log de mensagens com a mensagem do usuário ou assistente
    def update_message_log_user(self, conversation_model, log_mensagens):
        # Criar um novo log de mensagem com o papel (usuário ou assistente) e conteúdo da mensagem
        message_log = {"date_time": conversation_model.data_hora, "role": "user", "content": conversation_model.conversation}
        
        # Verifica se o número de telefone já está no dicionário
        if conversation_model.phone_number in log_mensagens:
            # Se já existir, atualiza o status e o nome
            log_mensagens[conversation_model.phone_number]["status_atendimento"] = conversation_model.status_atendimento
            log_mensagens[conversation_model.phone_number]["nome_cliente"] = conversation_model.nome_cliente
            log_mensagens[conversation_model.phone_number]["data_hora"] = conversation_model.data_hora
            log_mensagens[conversation_model.phone_number]["plataforma_origem"] = conversation_model.plataforma_origem
            
            # Se já existir, adiciona a mensagem de log ao dicionário existente        
            log_mensagens[conversation_model.phone_number]["messages"].append(message_log)
        else:
            # Log inicial com instruções e apresentação ao usuário
            initial_log = {"date_time": conversation_model.data_hora, "role": "system", "content": "Você é a Bela, assistente virtual do salão de beleza chamado Glowz Beauty Lounge",}  

            # Caso contrário, cria uma nova entrada no dicionário com o status e a mensagem de log
            log_mensagens[conversation_model.phone_number] = {
                "status_atendimento": conversation_model.status_atendimento.name,
                "nome_cliente": conversation_model.nome_cliente,
                "data_hora": conversation_model.data_hora,
                "plataforma_origem": conversation_model.plataforma_origem.name,                
                "messages": [initial_log, message_log]
            }
            
        # Nome do arquivo onde você deseja salvar o dicionário
        nome_arquivo = "log_mensagens.json"

        # Salvar o dicionário em um arquivo JSON
        with open(nome_arquivo, "w") as arquivo:
            json.dump(log_mensagens, arquivo)
            
        # Retornar o log de mensagens atualizado para o número de telefone
        return log_mensagens[conversation_model.phone_number]
    
    # Função para criar ou atualizar o log de mensagens com a mensagem do usuário ou assistente
    def update_message_log_assistant(self, conversation_model, log_mensagens):
        # Criar um novo log de mensagem com o papel (usuário ou assistente) e conteúdo da mensagem
        message_log = {"date_time": conversation_model.data_hora, "role": "assistant", "content": conversation_model.resposta}
        
        log_mensagens[conversation_model.phone_number]["status_atendimento"] = conversation_model.status_atendimento.name
        log_mensagens[conversation_model.phone_number]["nome_cliente"] = conversation_model.nome_cliente
        log_mensagens[conversation_model.phone_number]["data_hora"] = conversation_model.data_hora
        log_mensagens[conversation_model.phone_number]["plataforma_origem"] = conversation_model.plataforma_origem.name
        
        log_mensagens[conversation_model.phone_number]["messages"].append(message_log)
            
        # Nome do arquivo onde você deseja salvar o dicionário
        nome_arquivo = "log_mensagens.json"

        # Salvar o dicionário em um arquivo JSON
        with open(nome_arquivo, "w") as arquivo:
            json.dump(log_mensagens, arquivo)
            
        # Retornar o log de mensagens atualizado para o número de telefone
        return log_mensagens[conversation_model.phone_number]