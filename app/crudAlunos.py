from flask import Flask, request, jsonify
from flasgger import Swagger
import Util.bd as bd
import logging
import sys

# Criação do logger
logger = logging.getLogger("escola_infantil")
logger.setLevel(logging.DEBUG)

# Handler para arquivo (logs detalhados)
file_handler = logging.FileHandler("escola_infantil.log")
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)

# Handler para console (logs resumidos)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

app = Flask(__name__)

# Configuração do Swagger com melhorias
app.config['SWAGGER'] = {
    'title': 'API de Gerenciamento de Alunos da Escola',
    'uiversion': 3,
    'description': 'Esta API oferece operações CRUD para a gestão de alunos em um sistema escolar. Permite listar, cadastrar, atualizar e deletar informações de alunos.',
    'termsOfService': 'http://your-terms-of-service-url.com',
    'contact': {
        'name': 'Suporte da API',
        'url': 'http://your-support-url.com',
        'email': 'support@example.com'
    },
    'license': {
        'name': 'Apache 2.0',
        'url': 'http://www.apache.org/licenses/LICENSE-2.0.html'
    },
    'version': '1.0.0',
    'servers': [
        {'url': 'http://localhost:5000', 'description': 'Servidor de Desenvolvimento Local'}
    ],
    'specs': [
        {
            'endpoint': 'apispec_1',
            'route': '/apispec_1.json',
            'rule_filter': lambda rule: True,  # all in
            'model_filter': lambda tag: True,  # all in
        }
    ]
}

swagger = Swagger(app)

#Debug slq
@app.route('/tabelas', methods=['GET'])
def listar_tabelas():
    """
    Listar todas as tabelas do banco de dados
    ---
    tags:
      - Debug
    responses:
        200:
            description: Lista de tabelas obtida com sucesso
            schema:
                type: array
                items:
                    type: string
        500:
            description: Falha na conexão com o banco de dados
    """
    conn = bd.create_connection()
    if conn is None:
        logger.error("Falha na conexão com o banco de dados")
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
        logger.info("Operação GET concluída com sucesso")
        return jsonify(resultado), 200

    except Exception as e:
        logger.error("Erro ao processar solicitação: %s", str(e))
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

# Listar todos os alunos
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    """
    Listar todos os alunos
    Retorna uma lista de todos os alunos cadastrados.
    ---
    tags:
      - Alunos
    responses:
        200:
            description: Lista de alunos obtida com sucesso
            schema:
                type: array
                items:
                    type: object
                    properties:
                        aluno_id:
                            type: string
                        nome_completo:
                            type: string
                        data_nascimento:
                            type: string
                            format: date
                        id_turma:
                            type: integer
                        nome_responsavel:
                            type: string
                        telefone_responsavel:
                            type: string
                        email_responsavel:
                            type: string
                        informacoes_adicionais:
                            type: string
        500:
            description: Falha na conexão com o banco de dados
        400:
            description: Erro ao listar alunos
    """
    conn = bd.create_connection()
    if conn is None:
        logger.error("Falha na conexão com o banco de dados")
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM aluno")
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
        logger.info("Listagem de alunos realizada com sucesso: %s", resultado)
        return jsonify(resultado), 200

    except Exception as e:
        logger.error("Erro ao listar alunos: %s", str(e))
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

# Cadastrar um novo aluno
@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    """
    Cadastrar um novo aluno
    Permite cadastrar um novo aluno no sistema.
    ---
    tags:
      - Alunos
    parameters:
        - in: body
          name: aluno
          schema:
              type: object
              required:
                  - aluno_id
                  - nome_completo
                  - data_nascimento
                  - id_turma
                  - nome_responsavel
                  - telefone_responsavel
                  - email_responsavel
              properties:
                  aluno_id:
                      type: string
                      description: Identificador único do aluno
                  nome_completo:
                      type: string
                      description: Nome completo do aluno
                  data_nascimento:
                      type: string
                      format: date
                      description: Data de nascimento do aluno (YYYY-MM-DD)
                  id_turma:
                      type: integer
                      description: ID da turma do aluno
                  nome_responsavel:
                      type: string
                      description: Nome do responsável
                  telefone_responsavel:
                      type: string
                      description: Telefone do responsável
                  email_responsavel:
                      type: string
                      description: E-mail do responsável
                  informacoes_adicionais:
                      type: string
                      description: Informações adicionais sobre o aluno (opcional)
    responses:
        201:
            description: Aluno cadastrado com sucesso
        400:
            description: Dados inválidos ou erro ao cadastrar aluno
        500:
            description: Falha na conexão com o banco de dados
    """
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        logger.error("Falha na conexão com o banco de dados")
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO aluno (
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
        logger.info("Aluno cadastrado com sucesso: %s", data)
        return jsonify({"message": "Aluno cadastrado com sucesso"}), 201

    except Exception as e:
        conn.rollback()
        logger.error("Erro ao cadastrar aluno: %s", str(e))
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# Atualizar dados de um aluno existente
@app.route('/alunos/<string:aluno_id>', methods=['PUT'])
def atualizar_aluno(aluno_id):
    """
    Atualizar dados de um aluno existente
    Permite atualizar as informações de um aluno específico.
    ---
    tags:
      - Alunos
    parameters:
        - in: path
          name: aluno_id
          type: string
          required: true
          description: ID do aluno a ser atualizado
        - in: body
          name: aluno
          schema:
              type: object
              required:
                  - nome_completo
                  - data_nascimento
                  - id_turma
                  - nome_responsavel
                  - telefone_responsavel
                  - email_responsavel
              properties:
                  nome_completo:
                      type: string
                      description: Novo nome completo do aluno
                  data_nascimento:
                      type: string
                      format: date
                      description: Nova data de nascimento do aluno (YYYY-MM-DD)
                  id_turma:
                      type: integer
                      description: Novo ID da turma do aluno
                  nome_responsavel:
                      type: string
                      description: Novo nome do responsável
                  telefone_responsavel:
                      type: string
                      description: Novo telefone do responsável
                  email_responsavel:
                      type: string
                      description: Novo e-mail do responsável
                  informacoes_adicionais:
                      type: string
                      description: Novas informações adicionais sobre o aluno (opcional)
    responses:
        200:
            description: Aluno atualizado com sucesso
        400:
            description: Dados inválidos ou erro ao atualizar aluno
        500:
            description: Falha na conexão com o banco de dados
    """
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        logger.error("Falha na conexão com o banco de dados")
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE aluno SET
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
        logger.info("Aluno atualizado com sucesso: ID=%s, Dados=%s", aluno_id, data)
        return jsonify({"message": "Aluno atualizado com sucesso"}), 200

    except Exception as e:
        conn.rollback()
        logger.error("Erro ao atualizar aluno: %s", str(e))
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# Deletar um aluno
@app.route('/alunos/<string:aluno_id>', methods=['DELETE'])
def deletar_aluno(aluno_id):
    """
    Deletar um aluno
    Remove um aluno específico do sistema.
    ---
    tags:
      - Alunos
    parameters:
        - in: path
          name: aluno_id
          type: string
          required: true
          description: ID do aluno a ser deletado
    responses:
        200:
            description: Aluno deletado com sucesso
        400:
            description: Erro ao deletar aluno
        500:
            description: Falha na conexão com o banco de dados
    """
    conn = bd.create_connection()
    if conn is None:
        logger.error("Falha na conexão com o banco de dados")
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM aluno WHERE aluno_id = %s", (aluno_id,))
        conn.commit()
        logger.info("Aluno deletado com sucesso: ID=%s", aluno_id)
        return jsonify({"message": "Aluno deletado com sucesso"}), 200

    except Exception as e:
        conn.rollback()
        logger.error("Erro ao deletar aluno: %s", str(e))
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# Iniciar a aplicação Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)