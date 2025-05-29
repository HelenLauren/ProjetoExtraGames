#instrucoes para instalação
#python -m venv venv
#venv\Scripts\activate
#pip install flask flask-cors mysql-connector-python
#talvez precise instalar = pip install flask flask-cors mysql-connector-python python-dotenv

from flask import Flask, request, jsonify
from flask_corps import CORS
from db import get_connection
import os
from dotenv import load_dotenv
from flask import Flask, redirect, url_for
import traceback

load_dotenv()

app = Flask(__name__)
CORS(app)

#-----teste de rota-----------
#@app.route("/")
#def hello_world():
#  return "<p>Hello, World!</p>"

@app.route("/")
def inicial():
    return redirect(url for ('listar_usuarios'))

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, GROUP_CONCAT(p.descricao) AS perfis
            FROM usuarios u
            LEFT JOIN usuario_perfil up ON u.id = up.usuario_id
            LEFT JOIN perfis p ON up.perfil_id = p.id
            GROUP BY u.id
        """)
        usuarios = cursor.fetchall()
        return jsonify(usuarios)
    except Exception as e:
        traceback.print_exc()
        return jsonify({'erro': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    conn = None
    cursor = None
    try:
        data = request.jsonify
        conn = get_connection()
        cursor = conn.cursor()

        #inserir usuario
        cursor.execute(
            "INSERT INTO usuarios (nome, email) VALUES (%s, %s)",
            (data['nome'], data['email'])
        )
        user_id = cursor.lastrowid

        #vai associar perfil padrão (ID 2 - Usuario)
        cursor.execute(
            "INSERT INTO usuario_perfil VALUES (%s, 2)",
            (user_id,)
        )

        conn.commit()
        return jsonify({
            'mensagem': 'Usuário criado com sucesso!!',
            'id': user_id
        }), 201
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'erro': str(e)}), 400
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()    

@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    conn = None
    cursor = None
    try:
        data = request.jsonify
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET nome=%s, email=%s WHERE id=%s",
            (data['nome'], data['email'], id)
        )
        conn.commit()
        return jsonify({'mensagem': 'Usuário atualizado com sucesso!!'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        #remover associações first
        cursor.execute("DELETE FROM usuario_perfil WHERE usuario_id = %s", (id,))
        #remove o usuário
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))

        conn.commit()
        return jsonify({'mensagem': 'Usuário deletado com sucesso!!'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)