import psycopg
import os
from dotenv import load_dotenv
from psycopg import Error

load_dotenv()

def connect():
    try:
        conn = psycopg.connect(
        host = os.getenv("DB_HOST"),
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        port = os.getenv("DB_PORT")
    )
        print("Connected successfully!")
        return conn
        
    except Error as e:
        print(f"Connection error: {e}")
        return None
        
def close_connection(conn):
    if conn:
        conn.close()
        print("Connection closed!")