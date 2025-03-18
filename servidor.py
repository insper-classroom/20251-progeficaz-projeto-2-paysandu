from flask import Flask
from flask import request
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv('.env')


config = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': os.getenv('MYSQL_HOST'),
    'database': os.getenv('MYSQL_DATABASE'),
    'port': os.getenv('MYSQL_PORT'),
    'ssl_ca': os.getenv('MYSQL_SSL_CA'),
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

@app.route('/allimoveis')
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
@app.route('/imoveis/<int:id>')
def get_imovel(id):
    try:
        cunn = connect_db()
        if cunn:
            cursor = cunn.cursor()
            cursor.execute(f"SELECT * FROM imoveis WHERE id = {id}")
            data = cursor.fetchone()
            cunn.close()
            return {"imoveis": data}
        else:
            return {"erro": "Não foi possível conectar ao banco de dados"}
    except Error as err:
        return {"erro": f"Erro: {err}"}
    

@app.route('/imoveis', methods=['POST'])
def add_imovel():
    try:
        data = request.json
        cunn = connect_db()
        if cunn:
            cursor = cunn.cursor()
            cursor.execute(
                "INSERT INTO imoveis ( logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)",
                ( data['logradouro'], data['tipo_logradouro'], data['bairro'], data['cidade'], data['cep'], data['tipo'], data['valor'], data['data_aquisicao'])
            )
            cunn.commit()
            cunn.close()
            return data, 201
        else:
            return {"erro": "Não foi possível conectar ao banco de dados"}
    except Error as err:
        return {"erro": f"Erro: {err}"}
    except KeyError as key_err:
        return {"erro": f"Chave ausente: {key_err}"}
    
@app.route('/imoveis/<int:id>/update', methods=['PUT'])
def update_imovel(id):
    try:
        data = request.json
        cunn = connect_db()
        if cunn:
            cursor = cunn.cursor()
            cursor.execute(
                "UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s",
                (data['logradouro'], data['tipo_logradouro'], data['bairro'], data['cidade'], data['cep'], data['tipo'], data['valor'], data['data_aquisicao'], id)
            )
            cunn.commit()
            cunn.close()
            return data
        else:
            return {"erro": "Não foi possível conectar ao banco de dados"}
    except Error as err:
        return {"erro": f"Erro: {err}"}
    except KeyError as key_err:
        return {"erro": f"Chave ausente: {key_err}"}
    
@app.route('/imoveis/<int:id>/delete', methods=['DELETE'])
def delete_imovel(id):
    try:
        cunn = connect_db()
        if cunn:
            cursor = cunn.cursor()
            cursor.execute(f"DELETE FROM imoveis WHERE id = {id}")
            cunn.commit()
            cunn.close()
            return {"message": "Imóvel removido com sucesso"}
        else:
            return {"erro": "Não foi possível conectar ao banco de dados"}
    except Error as err:
        return {"erro": f"Erro: {err}"}
    
@app.route('/imoveis/tipo/<tipo>')
def get_imoveis_por_tipo(tipo):
    try:
        cunn = connect_db()
        if cunn:
            cursor = cunn.cursor()
            cursor.execute("SELECT * FROM imoveis WHERE tipo = %s", (tipo.replace('%20', ' '),))
            data = cursor.fetchall()
            cunn.close()
            return {"imoveis": data}
        else:
            return {"erro": "Não foi possível conectar ao banco de dados"}
    except Error as err:
        return {"erro": f"Erro: {err}"}
    
@app.route('/imoveis/cidade/<cidade>')
def get_imoveis_por_cidade(cidade):
    try:
        cunn = connect_db()
        if cunn:
            cursor = cunn.cursor()
            cursor.execute("SELECT * FROM imoveis WHERE cidade = %s", (cidade.replace('%20', ' '),))
            data = cursor.fetchall()
            cunn.close()
            return {"imoveis": data}
        else:
            return {"erro": "Não foi possível conectar ao banco de dados"}
    except Error as err:
        return {"erro": f"Erro: {err}"}
if __name__ == '__main__':
    app.run(debug=True)
