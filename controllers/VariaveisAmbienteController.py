import os
from dotenv import load_dotenv
load_dotenv()

class VariaveisAmbienteController:
    def __init__(self):
        self._API_ADDRESS = os.environ["API_ADDRESS"]
        self._API_KEY_WHATSAPP = os.environ["API_KEY_WHATSAPP"]
        self._API_KEY_OPENAI = os.environ["API_KEY_OPENAI"]
        self._INSTANCE = os.environ["INSTANCE"]
        self._DBNAME = os.environ["DBNAME"]
        self._DBUSER = os.environ["DBUSER"]
        self._DBPASSWORD = os.environ["DBPASSWORD"]
        self._DBHOST = os.environ["DBHOST"]

    @property
    def API_ADDRESS(self):
        return self._API_ADDRESS
    
    @property
    def API_KEY_WHATSAPP(self):
        return self._API_KEY_WHATSAPP
    
    @property
    def API_KEY_OPENAI(self):
        return self._API_KEY_OPENAI
    
    @property
    def INSTANCE(self):
        return self._INSTANCE

    @property
    def DBNAME(self):
        return self._DBNAME

    @property
    def DBUSER(self):
        return self._DBUSER

    @property
    def DBPASSWORD(self):
        return self._DBPASSWORD

    @property
    def DBHOST(self):
        return self._DBHOST