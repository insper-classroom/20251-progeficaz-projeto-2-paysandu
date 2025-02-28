from flask import Flask
import os
import mysql.connector
from mysql.connector import Error


config= {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': os.getenv('MYSQL_HOST'),
    'database': os.getenv('MYSQL_DATABASE')
}

def connect_db():
    try:
        # Tenta estabelecer a conexão com o banco de dados usando mysql-connector-python
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        # Em caso de erro, imprime a mensagem de erro
        print(f"Erro: {err}")
        return None

app = Flask(__name__)

@app.route('/')
def index():
    try:
        cunn = connect_db()
        if cunn:
            cursor = cunn.cursor()
            cursor.execute("SELECT * FROM imoveis")
            data = cursor.fetchall()
            cunn.close()
            return {"imoveis": data}
        else:
            return {"erro": "Não foi possível conectar ao banco de dados"}
    except Error as err:
        return {"erro": f"Erro: {err}"}
