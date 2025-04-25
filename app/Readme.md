
Este microserviço fornece uma API CRUD para a tabela `Aluno` do banco de dados PostgreSQL. Ele permite criar, ler, atualizar e deletar registros de alunos. Este repositório deve ser clonado pelos Alunos da UniFaat para trabalharem os outros aspectos da aplicação.

## Configuração

1. **Banco de Dados**: Certifique-se de que o banco de dados PostgreSQL está configurado e rodando. 
   - O script SQL `escola.sql` na pasta `BD` contém a definição da tabela `Aluno`.

2. **Parâmetros de Conexão**: Configure os parâmetros de conexão ao banco de dados no arquivo `paramsBD.yml` localizado em `app/Util/`.

```yaml
# Util/paramsBD.yml
db_name: "escola"
db_user: "faat"
db_password: "faat"
db_host: "localhost"
db_port: "5432"
```

## Execução

### Instalar Dependências
Certifique-se de que você tem o Flask, Flasgger e psycopg2 instalados. Você pode instalar as dependências usando o comando:
```sh
pip install -r requirements.txt
```

### Rodar o Microserviço
Navegue até o diretório raiz do projeto e execute o seguinte comando para iniciar o servidor Flask:
```sh
export FLASK_APP=crudAlunos
flask run --host=0.0.0.0 --port=5000
```

No Windows, use:
```sh
set FLASK_APP=crudAlunos
flask run --host=0.0.0.0 --port=5000
```

## Endpoints

### Listar Alunos
- **URL**: `/alunos`
- **Método**: `GET`
- **Descrição**: Retorna uma lista de todos os alunos cadastrados.
- **Exemplo de `curl`**:
  ```sh
  curl -X GET http://localhost:5000/alunos
  ```

### Cadastrar Aluno
- **URL**: `/alunos`
- **Método**: `POST`
- **Corpo da Requisição**:
  ```json
  {
      "aluno_id": "123",
      "nome_completo": "João Silva",
      "data_nascimento": "2000-01-01",
      "id_turma": "1",
      "nome_responsavel": "Maria Silva",
      "telefone_responsavel": "123456789",
      "email_responsavel": "maria@example.com",
      "informacoes_adicionais": "Nenhuma"
  }
  ```
- **Exemplo de `curl`**:
  ```sh
  curl -X POST http://localhost:5000/alunos \
  -H "Content-Type: application/json" \
  -d '{
      "aluno_id": "123",
      "nome_completo": "João Silva",
      "data_nascimento": "2000-01-01",
      "id_turma": "1",
      "nome_responsavel": "Maria Silva",
      "telefone_responsavel": "123456789",
      "email_responsavel": "maria@example.com",
      "informacoes_adicionais": "Nenhuma"
  }'
  ```

### Atualizar Aluno
- **URL**: `/alunos/<string:aluno_id>`
- **Método**: `PUT`
- **Corpo da Requisição**:
  ```json
  {
      "nome_completo": "João Silva Atualizado",
      "data_nascimento": "2000-01-01",
      "id_turma": "1",
      "nome_responsavel": "Maria Silva",
      "telefone_responsavel": "987654321",
      "email_responsavel": "maria@example.com",
      "informacoes_adicionais": "Atualizado"
  }
  ```
- **Exemplo de `curl`**:
  ```sh
  curl -X PUT http://localhost:5000/alunos/123 \
  -H "Content-Type: application/json" \
  -d '{
      "nome_completo": "João Silva Atualizado",
      "data_nascimento": "2000-01-01",
      "id_turma": "1",
      "nome_responsavel": "Maria Silva",
      "telefone_responsavel": "987654321",
      "email_responsavel": "maria@example.com",
      "informacoes_adicionais": "Atualizado"
  }'
  ```

### Deletar Aluno
- **URL**: `/alunos/<string:aluno_id>`
- **Método**: `DELETE`
- **Exemplo de `curl`**:
  ```sh
  curl -X DELETE http://localhost:5000/alunos/123
  ```

## Testes
Para rodar os testes automatizados com `pytest`, execute:
```sh
pytest
```
