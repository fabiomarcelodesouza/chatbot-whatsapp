# WhatsApp OpenAI Webhook

Este projeto tem como objetivo criar uma aplicação Python que integra a leitura de mensagens do WhatsApp com a API da OpenAI para fornecer respostas inteligentes. A aplicação é composta por várias classes, cada uma responsável por uma parte específica do processo.

## Classes e Funcionalidades

### `wp_audio.py`

Esta classe contém funções relacionadas ao processamento de mensagens de áudio no WhatsApp.

- `convert_audio_bytes(audio_bytes)`: Converte bytes de áudio Ogg para dados de áudio compatíveis com a biblioteca de reconhecimento de fala.
- `recognize_audio(audio_bytes)`: Realiza o reconhecimento de fala nos dados de áudio usando a API do Google.
- `handle_audio_message(audio_id)`: Lida com mensagens de áudio, convertendo-as para texto e retornando uma mensagem.

### `wp_handle.py`

Esta classe gerencia o processamento e tratamento das mensagens do WhatsApp.

- `handle_whatsapp_message(body)`: Lida com mensagens do WhatsApp de diferentes tipos, como texto e áudio, chamando funções específicas para cada tipo.
- `handle_message(request)`: Lida com mensagens recebidas via webhook, direcionando-as para as funções adequadas.

### `wp_media.py`

Esta classe fornece funcionalidades para interação com a API do WhatsApp para obtenção de URLs e download de arquivos de mídia.

- `get_media_url(media_id)`: Obtém a URL da mídia a partir do ID da mídia.
- `download_media_file(media_url)`: Baixa o arquivo de mídia a partir da URL fornecida.

### `wp_openai.py`

Esta classe integra a API da OpenAI para gerar respostas inteligentes.

- `update_message_log(message, phone_number, role)`: Cria ou atualiza um log de mensagens para permitir uma conversação contínua.
- `remove_last_message_from_log(phone_number)`: Remove a última mensagem do log em caso de falha na solicitação à OpenAI.
- `make_openai_request(message, from_number)`: Realiza uma solicitação à API da OpenAI para gerar uma resposta com base no histórico de mensagens.

### `wp_text.py`

Esta classe lida com mensagens de texto no WhatsApp, enviando respostas de volta aos usuários.

- `send_whatsapp_message(body, message)`: Envia a resposta como uma mensagem no WhatsApp de volta ao usuário.

### `wp_tools.py`

Esta classe contém funcionalidades para verificar e validar o webhook do WhatsApp.

- `verify_webhook(request)`: Verifica o token do webhook de acordo com as informações da solicitação.

### `app.py`

Este é o arquivo principal que configura o servidor Flask e define os endpoints para interação com o webhook do WhatsApp.

- `/`: Endpoint inicial que exibe uma mensagem de boas-vindas.
- `/webhook`: Endpoint principal para interação com mensagens do WhatsApp via webhook.
- `/reset`: Endpoint para redefinir o log de mensagens.

## Configuração do Ambiente

Antes de executar a aplicação, certifique-se de configurar as variáveis de ambiente necessárias, como as chaves da API do WhatsApp e OpenAI.

```bash
export API_KEY_WHATSAPP="sua_chave_api_whatsapp"
export API_KEY_OPENAI="sua_chave_api_openai"
export API_KEY_WHATSAPP_VERIFY_TOKEN="seu_token_verificacao_whatsapp"
```
## Dependências
Instale as bibliotecas necessárias utilizando o seguinte comando:

```bash
pip install -r requirements.txt
```

## Execução
Execute a aplicação com o seguinte comando:

```bash
python run app.py
```

Caso esteja executando localmente, a aplicação estará ouvindo em http://127.0.0.1:5000/ e para configurar seu webhook, você deverá utilizar uma ferramenta que crie um endpoint público, como o Ngrok por exemplo. Mais informações sobre o Ngrok podem ser obtidas em https://ngrok.com/.

**Observação**: Este README fornece uma visão geral da estrutura e funcionalidades da aplicação. Consulte a documentação específica das bibliotecas e APIs utilizadas para obter informações mais detalhadas.