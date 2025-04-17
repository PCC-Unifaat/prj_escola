from flask import Flask, request, jsonify
import Util.bd as bd

app = Flask(__name__)

# Listar todos os alunos
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Aluno")
        alunos = cursor.fetchall()
        return jsonify([
            {
                "aluno_id": aluno[0],
                "nome_completo": aluno[1],
                "data_nascimento": aluno[2],
                "id_turma": aluno[3],
                "nome_responsavel": aluno[4],
                "telefone_responsavel": aluno[5],
                "email_responsavel": aluno[6],
                "informacoes_adicionais": aluno[7]
            } for aluno in alunos
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# Cadastrar novo aluno
@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Aluno (aluno_id, nome_completo, data_nascimento, id_turma, nome_responsavel, telefone_responsavel, email_responsavel, informacoes_adicionais)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (data['aluno_id'], data['nome_completo'], data['data_nascimento'], data['id_turma'],
             data['nome_responsavel'], data['telefone_responsavel'], data['email_responsavel'], data.get('informacoes_adicionais'))
        )
        conn.commit()
        return jsonify({"message": "Aluno cadastrado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# Alterar dados de um aluno específico
@app.route('/alunos/<string:aluno_id>', methods=['PUT'])
def alterar_aluno(aluno_id):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE Aluno
            SET nome_completo = %s, data_nascimento = %s, id_turma = %s, nome_responsavel = %s, 
            telefone_responsavel = %s, email_responsavel = %s, informacoes_adicionais = %s
            WHERE aluno_id = %s
            """,
            (data['nome_completo'], data['data_nascimento'], data['id_turma'], data['nome_responsavel'],
             data['telefone_responsavel'], data['email_responsavel'], data.get('informacoes_adicionais'), aluno_id)
        )
        conn.commit()
        return jsonify({"message": "Dados do aluno atualizados com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# Excluir um aluno
@app.route('/alunos/<string:aluno_id>', methods=['DELETE'])
def excluir_aluno(aluno_id):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Aluno WHERE aluno_id = %s", (aluno_id,))
        conn.commit()
        return jsonify({"message": "Aluno excluído com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)