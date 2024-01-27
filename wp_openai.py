# Importando biblioteca necessária
from dotenv import load_dotenv
load_dotenv()
import os
from openai import OpenAI

# Chave da API do OpenAI
client = OpenAI(api_key=os.environ["API_KEY_OPENAI"])

# Dicionário de log de mensagens para permitir conversação ao longo de várias mensagens
message_log_dict = {}

# Função para criar ou atualizar o log de mensagens com a mensagem do usuário ou assistente
def update_message_log(message, phone_number, role):
    # Log inicial com instruções e apresentação ao usuário
    
    initial_log = {
        "role": "system",
        "content": """Você é a Bela, assistente virtual do salão de beleza chamado Glowz Beauty Lounge. No primeiro contato, apresente o salão de forma positiva usando até 20 palavras. Em seguida, retorne: 
        
        Como posso te ajudar hoje? 
        
        1 - Agendar um procedimento. 
        2 - Conversar sobre dicas de beleza. 
        3 - Falar com uma atendente humana.""",
    }
    
    # Criar um novo log de mensagem com o papel (usuário ou assistente) e conteúdo da mensagem
    message_log = {"role": role, "content": message}
    # Adicionar o log de mensagem ao dicionário usando o número de telefone como chave
    if phone_number not in message_log_dict:
        message_log_dict[phone_number] = [initial_log]
    message_log_dict[phone_number].append(message_log)
    # Retornar o log de mensagens atualizado para o número de telefone
    return message_log_dict[phone_number]

# Função para remover a última mensagem do log se a solicitação ao OpenAI falhar
def remove_last_message_from_log(phone_number):
    message_log_dict[phone_number].pop()

# Função para fazer uma solicitação ao OpenAI e obter uma resposta
def make_openai_request(message, from_number):
    try:
        # Atualizar o log de mensagens com a mensagem do usuário
        message_log = update_message_log(message, from_number, "user")
        # Fazer uma solicitação à API do OpenAI para completar o diálogo
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message_log
        )
        # Obter a resposta gerada pelo modelo
        response_message = response.choices[0].message.content
        print(f"Resposta do OpenAI: {response_message}")
        # Atualizar o log de mensagens com a resposta do assistente
        update_message_log(response_message, from_number, "assistant")
    except Exception as e:
        # Em caso de erro, informar e retornar uma mensagem padrão
        print(f"Erro do OpenAI: {e}")
        response_message = "Desculpe, a API do OpenAI está atualmente sobrecarregada ou offline. Por favor, tente novamente mais tarde."
        # Remover a última mensagem do log para evitar inconsistências
        remove_last_message_from_log(from_number)
    # Retornar a resposta gerada pelo modelo
    return response_message
