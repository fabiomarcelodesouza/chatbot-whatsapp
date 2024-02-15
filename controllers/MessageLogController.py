import json
from controllers.VariaveisAmbienteController import VariaveisAmbienteController

class MessageLogController:
    def __init__(self):
        pass

    # Função para criar ou atualizar o log de mensagens com a mensagem do usuário ou assistente
    def update_message_log(self, message, phone_number, role, status_atendimento, nome_cliente, log_mensagens):
        # Criar um novo log de mensagem com o papel (usuário ou assistente) e conteúdo da mensagem
        message_log = {"role": role, "content": message}
        
        # Verifica se o número de telefone já está no dicionário
        if phone_number in log_mensagens:
            # Se já existir, atualiza o status e o nome
            log_mensagens[phone_number]["status_atendimento"] = status_atendimento
            log_mensagens[phone_number]["nome_cliente"] = nome_cliente
            
            # Se já existir, adiciona a mensagem de log ao dicionário existente        
            log_mensagens[phone_number]["messages"].append(message_log)
        else:
            # Log inicial com instruções e apresentação ao usuário
            initial_log = {"role": "system", "content": "Você é a Bela, assistente virtual do salão de beleza chamado Glowz Beauty Lounge",}  

            # Caso contrário, cria uma nova entrada no dicionário com o status e a mensagem de log
            log_mensagens[phone_number] = {
                "status_atendimento": status_atendimento,
                "nome_cliente": nome_cliente,
                "messages": [initial_log, message_log]
            }
            
        # Nome do arquivo onde você deseja salvar o dicionário
        nome_arquivo = "log_mensagens.json"

        # Salvar o dicionário em um arquivo JSON
        with open(nome_arquivo, "w") as arquivo:
            json.dump(log_mensagens, arquivo)
            
        # Retornar o log de mensagens atualizado para o número de telefone
        return log_mensagens[phone_number]