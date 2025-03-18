from flask import Flask, request, jsonify, abort
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
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
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
            return jsonify({"imoveis": data})
        else:
            abort(500, description="Não foi possível conectar ao banco de dados")
    except Error as err:
        abort(500, description=f"Erro: {err}")

@app.route('/imoveis/<int:id>')
def get_imovel(id):
    try:
        cunn = connect_db()
        if cunn:
            cursor = cunn.cursor()
            cursor.execute("SELECT * FROM imoveis WHERE id = %s", (id,))
            data = cursor.fetchone()
            cunn.close()
            if data:
                return jsonify({"imoveis": data})
            else:
                abort(404, description="Imóvel não encontrado")
        else:
            abort(500, description="Não foi possível conectar ao banco de dados")
    except Error as err:
        abort(500, description=f"Erro: {err}")

@app.route('/imoveis', methods=['POST'])
def add_imovel():
    try:
        data = request.json
        cunn = connect_db()
        if cunn:
            cursor = cunn.cursor()
            cursor.execute(
                "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (data['logradouro'], data['tipo_logradouro'], data['bairro'], data['cidade'], data['cep'], data['tipo'], data['valor'], data['data_aquisicao'])
            )
            cunn.commit()
            cunn.close()
            return jsonify(data), 201
        else:
            abort(500, description="Não foi possível conectar ao banco de dados")
    except Error as err:
        abort(500, description=f"Erro: {err}")
    except KeyError as key_err:
        abort(400, description=f"Chave ausente: {key_err}")

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
            return jsonify(data),201
        else:
            abort(500, description="Não foi possível conectar ao banco de dados")
    except Error as err:
        abort(500, description=f"Erro: {err}")
    except KeyError as key_err:
        abort(400, description=f"Chave ausente: {key_err}")

@app.route('/imoveis/<int:id>/delete', methods=['DELETE'])
def delete_imovel(id):
    try:
        cunn = connect_db()
        if cunn:
            cursor = cunn.cursor()
            cursor.execute("DELETE FROM imoveis WHERE id = %s", (id,))
            cunn.commit()
            cunn.close()
            return jsonify({"message": "Imóvel removido com sucesso"})
        else:
            abort(500, description="Não foi possível conectar ao banco de dados")
    except Error as err:
        abort(500, description=f"Erro: {err}")

@app.route('/imoveis/tipo/<tipo>')
def get_imoveis_por_tipo(tipo):
    try:
        cunn = connect_db()
        if cunn:
            cursor = cunn.cursor()
            cursor.execute("SELECT * FROM imoveis WHERE tipo = %s", (tipo.replace('%20', ' '),))
            data = cursor.fetchall()
            cunn.close()
            return jsonify({"imoveis": data})
        else:
            abort(500, description="Não foi possível conectar ao banco de dados")
    except Error as err:
        abort(500, description=f"Erro: {err}")

@app.route('/imoveis/cidade/<cidade>')
def get_imoveis_por_cidade(cidade):
    try:
        cunn = connect_db()
        if cunn:
            cursor = cunn.cursor()
            cursor.execute("SELECT * FROM imoveis WHERE cidade = %s", (cidade.replace('%20', ' '),))
            data = cursor.fetchall()
            cunn.close()
            return jsonify({"imoveis": data})
        else:
            abort(500, description="Não foi possível conectar ao banco de dados")
    except Error as err:
        abort(500, description=f"Erro: {err}")

if __name__ == '__main__':
    app.run(debug=True)
