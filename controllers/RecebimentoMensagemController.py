import json
from flask import jsonify
from controllers.AtendimentoPorTextoController import AtendimentoPorTextoController

class RecebimentoMensagemController:
    # Dicionário de log de mensagens para permitir conversação ao longo de várias mensagens
    def __init__(self,):
        pass
    
    # Função para lidar com mensagens recebidas via webhook
    def recebe_mensagem(self, request, log_mensagens):
        # Analisar o corpo da requisição no formato json
        body = request.get_json()

        try:
            json_conversation, codigo_retorno = self.obtem_json_recebido(body)

            if codigo_retorno == 200:                
                self.recebe_mensagem_whatsapp(json_conversation, log_mensagens)
                return jsonify({"status": "ok"}), 200
            else:
                # Se a requisição não for um evento da API do WhatsApp ou um evento nao mapeado, retornar um erro
                print(f"Exceção: {json_conversation}")
                return json_conversation, codigo_retorno
        # Capturar todos os outros erros e retornar um erro interno do servidor
        except Exception as e:
            print(f"Erro desconhecido: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    # Função para lidar com mensagens do WhatsApp de diferentes tipos
    def recebe_mensagem_whatsapp(self, json_conversation, log_mensagens):
        atendimento_texto_controller = AtendimentoPorTextoController()

        conversation = json_conversation["conversation"]
        phone_number = json_conversation["phone_number"]

        phone_number = phone_number.replace('@s.whatsapp.net', '')
        
        # Inicio de conversa              
        if phone_number not in log_mensagens:        
            atendimento_texto_controller.inicia_atendimento(conversation, phone_number, log_mensagens)
        
        # Conversa inciada e usuario não identificado
        elif log_mensagens[phone_number]["status"] == "iniciado":
            atendimento_texto_controller.confirma_cadastro(conversation, phone_number, log_mensagens)

        # Conversa inciada, usuario não identificado e esta em processo de confirmacao do cadastro
        elif (self.log_mensagens[phone_number]["status"] == "iniciando_cadastro" or
            self.log_mensagens[phone_number]["status"] == "confirmando_cadastro"):
            print(f'ABOBORAAAAAAAAAAAAAAA       {self.log_mensagens[phone_number]["status"]}')
            AtendimentoPorTextoController.cadastra_usario(body, conversation, phone_number, self.log_mensagens, "confirmando_cadastro")        

        
        print(self.log_mensagens)

        # if cliente_identificado:            




            # if body["data"]["message"]["conversation"]:
            #     message = {
            #         "text": {
            #             "body": body["data"]["message"]["conversation"]
            #         },
            #         "type": "text",
            #         "from": body["data"]["key"]["phone_number"]
            #     }
            # message_body = message["text"]["body"]
        # if message["type"] == "text":
        #     # Se a mensagem for do tipo texto, obter o corpo da mensagem
        #     message_body = message["text"]["body"]
        # elif message["type"] == "audio":
        #     # Se a mensagem for do tipo áudio, obter o ID do áudio e processar a mensagem de áudio
        #     audio_id = message["audio"]["id"]
        #     message_body = c_audio.handle_audio_message(audio_id)
        # # Fazer uma requisição ao OpenAI com o corpo da mensagem e o número do remetente
        # response = c_openai.make_openai_request(message_body, message["from"])
        # # Enviar a resposta via mensagem de texto no WhatsApp
        

    def obtem_json_recebido(self, body):
        if body.get("event") == "messages.upsert":
            if (
                body["data"]["message"].get("conversation")
                or body["data"]["message"]["extendedTextMessage"].get("text")
            ):  
                conversation = (
                    body["data"]["message"].get("conversation") or
                    body["data"]["message"]["extendedTextMessage"].get("text")
                )

                json_retorno = {
                                "phone_number": body["data"]["key"]["remoteJid"],
                                "conversation": conversation
                               }
                
                codigo_retorno = 200
            else:
                json_retorno = {"status": "Tag conversation ou remoteJid não encontrada"}
                codigo_retorno = 400
        else:
            json_retorno = {"status": "Evento não mapeado"}
            codigo_retorno = 204

        return json_retorno, codigo_retorno

   
