import psycopg2
from controllers.VariaveisAmbienteController import VariaveisAmbienteController
from utils.Enums.StatusAtendimento import StatusAtendimento

class DatabaseModel:
    def __init__(self):
        pass
    
    @staticmethod
    def database_connection():
        conn = None
        try:
            variaveis_ambiente_controller = VariaveisAmbienteController()

            conn = psycopg2.connect(
                dbname = variaveis_ambiente_controller.DBNAME,
                user = variaveis_ambiente_controller.DBUSER,
                password = variaveis_ambiente_controller.DBPASSWORD,
                host = variaveis_ambiente_controller.DBHOST
            )
            retorno = "Conectado com sucesso."
            status = 200
        except psycopg2.Error as e:
            retorno, status = f"Erro ao conectar no banco de dados - {e}", 500 
        
        return conn, retorno, status

    def identifica_cliente(self, phone_number): 
        conn_info = DatabaseModel.database_connection()
        if conn_info[0] is None:  # Verifica se a conexão é None
            raise psycopg2.Error(conn_info[1])

        conn, retorno, status = conn_info  # Desempacota a tupla
        cursor = conn.cursor()
        try:
            cursor.execute(f"select nome from cliente where phone_number = '{phone_number}'")

            registros = cursor.fetchall()
            registros_encontrados = len(registros)         

            if registros_encontrados == 0:
                retorno, status = "", 404
            elif registros_encontrados > 1:
                retorno, status = f'Foram encontrados {registros_encontrados} registros para o cliente {phone_number}.', 409
            else:
                retorno, status = registros[0][0], 200

        except psycopg2.Error as e:
            retorno, status = f"Erro ao realizar a consulta - {e}", 500        

        cursor.close()
        conn.close()

        return retorno, status

    def obtem_mensagens(self, status_atendimento):
        conn_info = DatabaseModel.database_connection()
        if conn_info[0] is None:  # Verifica se a conexão é None
            raise psycopg2.Error(conn_info[1])

        conn, retorno, status = conn_info  # Desempacota a tupla

        cursor = conn.cursor()
        try:
            cursor.execute(f"select descricao_mensagem from mensagem where id_mensagem_categoria = {status_atendimento.value}")
            retorno = cursor.fetchall()
            status = 200
        except psycopg2.Error as e:
            retorno, status = f"Erro ao realizar a consulta - {e}", 500        

        cursor.close()
        conn.close()

        return retorno, status

    def cadastrar_cliente(self, nome_cliente, phone_number):
        conn_info = DatabaseModel.database_connection()
        if conn_info[0] is None:  # Verifica se a conexão é None
            raise psycopg2.Error(conn_info[1])

        conn, retorno, status = conn_info  # Desempacota a tupla

        cursor = conn.cursor()
        try:
            cursor.execute(f"INSERT INTO cliente (nome, phone_number) VALUES (%s, %s)", (nome_cliente, phone_number))
            conn.commit()  # É necessário fazer commit após a inserção
            retorno = "Cliente cadastrado com sucesso"
            status = 200
        except psycopg2.Error as e:
            retorno, status = f"Erro ao realizar a consulta - {e}", 500        

        cursor.close()
        conn.close()

        return retorno, status
