import datetime


class ConversationModel:
    def __init__(self):        
        self._data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._resposta = ""

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        self._phone_number = value

    @property
    def status_atendimento(self):
        return self._status_atendimento

    @status_atendimento.setter
    def status_atendimento(self, value):
        self._status_atendimento = value

    @property
    def nome_cliente(self):
        return self._nome_cliente

    @nome_cliente.setter
    def nome_cliente(self, value):
        self._nome_cliente = value
        
    @property
    def data_hora(self):
        return self._data_hora

    @property
    def plataforma_origem(self):
        return self._plataforma_origem

    @plataforma_origem.setter
    def plataforma_origem(self, value):
        self._plataforma_origem = value

    @property
    def conversation(self):
        return self._conversation

    @conversation.setter
    def conversation(self, value):
        self._conversation = value

    @property
    def resposta(self):
        return self._resposta

    @resposta.setter
    def resposta(self, value):
        self._resposta = value

    @property
    def messages(self):
        return self._messages

    @messages.setter
    def messages(self, value):
        self._messages = value

    @property
    def mensagem_retorno(self):
        return self._mensagem_retorno

    @mensagem_retorno.setter
    def mensagem_retorno(self, value):
        self._mensagem_retorno = value