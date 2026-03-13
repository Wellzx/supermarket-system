import psycopg
import os
from dotenv import load_dotenv
from psycopg import Error

load_dotenv()

def conexao():
    try:
        conn = psycopg.connect(
        host = os.getenv("DB_HOST"),
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        port = os.getenv("DB_PORT")
    )
        print("Conectado com sucesso!")
        return conn
        
    except Error as e:
        print(f"Erro ao conectar: {e}")
        return None
        
def encerra_conexao(conn):
    if conn:
        conn.close()
        print("Conexão encerrada com o banco de dados!")