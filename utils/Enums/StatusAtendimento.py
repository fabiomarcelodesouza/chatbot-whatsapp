from enum import Enum

class StatusAtendimento(Enum):
    ClienteIdentificado = 1
    ClienteNaoIdentificado = 2
    ConfirmandoCadastro = 3
    CadastroNaoConfirmado = 4
    CadastroConfirmado = 5
    DadosConfirmacaoInvalidos = 6