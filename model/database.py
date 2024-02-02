import psycopg2

def database_connection():
    try:
        conn = psycopg2.connect(
            dbname="chatbot-glowz",
            user="postgres",
            password="123456",
            host="localhost"
        )
        retorno = "Conectado com sucesso."
        status = 200
    except psycopg2.Error as e:
        retorno, status = f"Erro ao conectar no banco de dados: {e}", 500 
    
    return conn, retorno, status

def identifica_cliente(phone_number):
    conn = database_connection()[0]
    cursor = conn.cursor()

    try:
        cursor.execute(f"select nome from cliente where phone_number = '{phone_number}'")
        registros = cursor.fetchall()
        registros_encontrados = len(registros)         

        if registros_encontrados == 0:
            retorno, status = "Cliente não encontrado", 404
        elif registros_encontrados > 1:
            retorno, status = f'Foram encontrados {registros_encontrados} registros para o cliente {phone_number}.', 409
        else:
            retorno, status = registros[0][0], 200

    except psycopg2.Error as e:
        retorno, status = f"Erro ao realizar a consulta: {e}", 500        

    cursor.close()
    conn.close()

    return retorno, status

def obtem_mensagens_saudacao(cliente_identificado):
    id_mensagem_categoria = 1 if cliente_identificado else 2

    conn = database_connection()[0]
    cursor = conn.cursor()

    try:
        cursor.execute(f"select descricao_mensagem from mensagem where id_mensagem_categoria = {id_mensagem_categoria}")
        retorno = cursor.fetchall()
        status = 200
    except psycopg2.Error as e:
        retorno, status = f"Erro ao realizar a consulta: {e}", 500        

    cursor.close()
    conn.close()

    return retorno, status