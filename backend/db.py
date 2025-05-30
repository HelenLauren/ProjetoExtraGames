import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            auth_plugin='mysql_native_password'
        )
    except mysql.connector.Error as err:
        print(f"Erro de conexão: {err}")
        raise    
    