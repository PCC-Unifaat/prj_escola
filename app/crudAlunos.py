from flask import Flask, request, jsonify
from flasgger import Swagger
import Util.bd as bd

app = Flask(__name__)

# Configuração do Swagger
swagger = Swagger(app)

#Debug slq
@app.route('/tabelas', methods=['GET'])
def listar_tabelas():
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        tabelas = cursor.fetchall()
        cursor.close()

        resultado = [tabela[0] for tabela in tabelas]
        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

# Listar todos os alunos
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Aluno")
        alunos = cursor.fetchall()
        cursor.close()

        resultado = []
        for aluno in alunos:
            resultado.append({
                "aluno_id": aluno[0],
                "nome_completo": aluno[1],
                "data_nascimento": aluno[2],
                "id_turma": aluno[3],
                "nome_responsavel": aluno[4],
                "telefone_responsavel": aluno[5],
                "email_responsavel": aluno[6],
                "informacoes_adicionais": aluno[7],
            })

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()


# Cadastrar um novo aluno
@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Aluno (
                aluno_id, nome_completo, data_nascimento, id_turma,
                nome_responsavel, telefone_responsavel, email_responsavel, informacoes_adicionais
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                data['aluno_id'],
                data['nome_completo'],
                data['data_nascimento'],
                data['id_turma'],
                data['nome_responsavel'],
                data['telefone_responsavel'],
                data['email_responsavel'],
                data.get('informacoes_adicionais', '')
            )
        )
        conn.commit()
        return jsonify({"message": "Aluno cadastrado com sucesso"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


# Atualizar dados de um aluno existente
@app.route('/alunos/<string:aluno_id>', methods=['PUT'])
def atualizar_aluno(aluno_id):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE Aluno SET
                nome_completo = %s,
                data_nascimento = %s,
                id_turma = %s,
                nome_responsavel = %s,
                telefone_responsavel = %s,
                email_responsavel = %s,
                informacoes_adicionais = %s
            WHERE aluno_id = %s
            """,
            (
                data['nome_completo'],
                data['data_nascimento'],
                data['id_turma'],
                data['nome_responsavel'],
                data['telefone_responsavel'],
                data['email_responsavel'],
                data.get('informacoes_adicionais', ''),
                aluno_id
            )
        )
        conn.commit()
        return jsonify({"message": "Aluno atualizado com sucesso"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


# Deletar um aluno
@app.route('/alunos/<string:aluno_id>', methods=['DELETE'])
def deletar_aluno(aluno_id):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Aluno WHERE aluno_id = %s", (aluno_id,))
        conn.commit()
        return jsonify({"message": "Aluno deletado com sucesso"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


# Iniciar a aplicação Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
