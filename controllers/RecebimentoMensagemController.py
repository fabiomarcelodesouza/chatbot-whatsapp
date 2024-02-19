import json
from flask import jsonify
from controllers.AtendimentoPorTextoController import AtendimentoPorTextoController
from utils.Enums.StatusAtendimento import StatusAtendimento
from utils.Enums.PlataformaOrigem import PlataformaOrigem
from models.ConversationModel import ConversationModel

class RecebimentoMensagemController:
    # Dicionário de log de mensagens para permitir conversação ao longo de várias mensagens
    def __init__(self):
        pass
    
    # Função para lidar com mensagens recebidas via webhook
    def recebe_mensagem(self, request, log_mensagens):
        # Analisar o corpo da requisição no formato json
        body = request.get_json()

        try:
            conversation_model, codigo_retorno = self.trata_json_recebido(body)

            if codigo_retorno == 200 and conversation_model.plataforma_origem == PlataformaOrigem.WhatsApp:
                self.recebe_mensagem_whatsapp(conversation_model, log_mensagens)
                return jsonify({"status": "ok"}), 200
            else:
                # Se a requisição não for um evento da API do WhatsApp ou um evento nao mapeado, retornar um erro
                print(f"Exceção: {conversation_model.mensagem_retorno}")
                return jsonify({"status": conversation_model.mensagem_retorno}), codigo_retorno
            
        # Capturar todos os outros erros e retornar um erro interno do servidor
        except Exception as e:
            print(f"Erro desconhecido: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    # Função para lidar com mensagens do WhatsApp de diferentes tipos
    def recebe_mensagem_whatsapp(self, conversation_model, log_mensagens):
        atendimento_texto_controller = AtendimentoPorTextoController()

        conversation_model.phone_number = conversation_model.phone_number.replace('@s.whatsapp.net', '')
        
        # Inicio de conversa              
        if conversation_model.phone_number not in log_mensagens:        
            atendimento_texto_controller.inicia_atendimento(conversation_model, log_mensagens)
        
        # # Envio de mensagem de confirmação de cadastro para cliente não identificado
        # elif log_mensagens[phone_number]["status_atendimento"] == StatusAtendimento.ClienteNaoIdentificado.name:
        #     atendimento_texto_controller.confirmando_cadastro(conversation, phone_number, log_mensagens)

        # # Cadastro confirmado pelo cliente
        # elif (log_mensagens[phone_number]["status_atendimento"] == StatusAtendimento.ConfirmandoCadastro.name
        #       or log_mensagens[phone_number]["status_atendimento"] == StatusAtendimento.DadosConfirmacaoInvalidos.name):
        #     if (conversation == '1' or conversation.lower() == "sim"):
        #         atendimento_texto_controller.cadastro_confirmado(conversation, phone_number, log_mensagens)
        #     elif (conversation == '2' or conversation.lower() == "não" or conversation.lower() == "nao"):
        #         atendimento_texto_controller.cadastro_nao_confirmado(conversation, phone_number, log_mensagens)
        #     else:
        #         atendimento_texto_controller.opcao_confirmacao_invalida(conversation, phone_number, log_mensagens)

        # # Cliente inserindo o nome novamente
        # elif log_mensagens[phone_number]["status_atendimento"] == StatusAtendimento.CadastroNaoConfirmado.name:
        #     atendimento_texto_controller.cadastro_nao_confirmado(conversation, phone_number, log_mensagens)

        # # Cliente identificado
        # elif log_mensagens[phone_number]["status_atendimento"] == StatusAtendimento.ClienteIdentificado.name:
        #     atendimento_texto_controller.cliente_identificado(conversation, phone_number, log_mensagens)


    def trata_json_recebido(self, body):
        conversation_model = ConversationModel()

        if body.get("event") in {"messages.upsert", "chats.update"}:
            if (
                body["data"]["message"].get("conversation")
                or body["data"]["message"]["extendedTextMessage"].get("text")
            ):  
                conversation = (
                    body["data"]["message"].get("conversation") or
                    body["data"]["message"]["extendedTextMessage"].get("text")
                )

                conversation_model.phone_number = body["data"]["key"]["remoteJid"]
                conversation_model.conversation = conversation
                conversation_model.plataforma_origem = PlataformaOrigem.WhatsApp

                codigo_retorno = 200
            else:
                conversation_model.mensagem_retorno = "Tag conversation ou remoteJid não encontrada"
                conversation_model.plataforma_origem = PlataformaOrigem.WhatsApp
                codigo_retorno = 400
        else:
            conversation_model.mensagem_retorno = "Evento não mapeado"
            conversation_model.plataforma_origem = PlataformaOrigem.WhatsApp
            codigo_retorno = 204

        return conversation_model, codigo_retorno

   
