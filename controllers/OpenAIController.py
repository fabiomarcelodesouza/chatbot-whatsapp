from openai import OpenAI

class OpenAIController: 
    # Função para criar ou atualizar o log de mensagens com a mensagem do usuário ou assistente
    def update_message_log(self, message, phone_number, role, log_mensagens):  
        # Criar um novo log de mensagem com o papel (usuário ou assistente) e conteúdo da mensagem
        message_log = {"role": role, "content": message}

        log_mensagens[phone_number].append(message_log)
        # Retornar o log de mensagens atualizado para o número de telefone
        return log_mensagens[phone_number]

    # Função para remover a última mensagem do log se a solicitação ao OpenAI falhar
    def remove_last_message_from_log(self, phone_number, log_mensagens):
        log_mensagens[phone_number].pop()

    # Função para fazer uma solicitação ao OpenAI e obter uma resposta
    def make_openai_request(self, message, from_number):
        try:
            # Atualizar o log de mensagens com a mensagem do usuário
            message_log = self.update_message_log(message, from_number, "user")
            # Fazer uma solicitação à API do OpenAI para completar o diálogo
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages = message_log
            )

            # Obter a resposta gerada pelo modelo
            response_message = response.choices[0].message.content
            print(f"Resposta do OpenAI: {response.choices[0].message.content}")

            # Atualizar o log de mensagens com a resposta do assistente
            self.update_message_log(response_message, from_number, "assistant")
        except Exception as e:
            # Em caso de erro, informar e retornar uma mensagem padrão
            print(f"Erro do OpenAI: {e}")
            response_message = "Desculpe, a API do OpenAI está atualmente sobrecarregada ou offline. Por favor, tente novamente mais tarde."
            # Remover a última mensagem do log para evitar inconsistências
            self.remove_last_message_from_log(from_number)
        # Retornar a resposta gerada pelo modelo
        return response_message
