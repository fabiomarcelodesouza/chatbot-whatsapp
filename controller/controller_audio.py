# Importando bibliotecas e módulos necessários
import pydub
import io
import soundfile as sf
import speech_recognition as sr
import controller_media as c_media
import langid

# Idioma padrão para reconhecimento de fala para texto
# TODO: Detectar automaticamente com base na preferência ou contexto do usuário
LANGUAGE = "pt-BR"

# Função para converter bytes de áudio ogg para dados de áudio compatíveis com a biblioteca de reconhecimento de fala
def convert_audio_bytes(audio_bytes):
    # Converter bytes de áudio ogg para AudioSegment
    ogg_audio = pydub.AudioSegment.from_ogg(io.BytesIO(audio_bytes))
    # Definir a largura da amostra para 4 bytes
    ogg_audio = ogg_audio.set_sample_width(4)
    # Exportar áudio ogg como wav e ler os bytes resultantes
    wav_bytes = ogg_audio.export(format="wav").read()
    # Ler os bytes wav e obter dados de áudio e taxa de amostragem usando a biblioteca soundfile
    audio_data, sample_rate = sf.read(io.BytesIO(wav_bytes), dtype="int32")
    sample_width = audio_data.dtype.itemsize
    # Criar um objeto AudioData a partir dos dados de áudio, taxa de amostragem e largura da amostra
    audio = sr.AudioData(audio_data, sample_rate, sample_width)
    return audio

# Função para realizar o reconhecimento de fala no dado de áudio fornecido
def recognize_audio(audio_bytes):
    # Inicializar um reconhecedor de fala
    recognizer = sr.Recognizer()
    # Reconhecer o áudio usando a API de reconhecimento de fala do Google, especificando o idioma
    audio_text = recognizer.recognize_google(audio_bytes, language=LANGUAGE)
    return audio_text

# Função para lidar com mensagens de áudio
def handle_audio_message(audio_id):
    # Obter a URL da mídia para o arquivo de áudio usando o módulo cmedia
    audio_url = c_media.get_media_url(audio_id)
    # Baixar o arquivo de áudio usando o módulo cmedia
    audio_bytes = c_media.download_media_file(audio_url)
    # Converter os bytes de áudio baixados para dados de áudio
    audio_data = convert_audio_bytes(audio_bytes)   
    # Reconhecer o texto dos dados de áudio
    audio_text = recognize_audio(audio_data)
    # Criar uma mensagem com o texto reconhecido e informações de idioma
    message = (
        f"Por favor, siga as instruções da seguinte mensagem em seu idioma original: {audio_text}"
    )

    return message
