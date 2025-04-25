# Projeto do Prof. Alexandre Tavares

## Estrutura do Projeto

├── BD/ # Contém os arquivos Docker para subir o Banco de Dados<br>
│ ├── escola.sql # SQL utilizado para criar o Banco e as tabelas utilizadas no projeto<br> 
│ ├── Dockerfile # Arquivo Docker para inicializar o PostgreSQL<br>
│ └── [Readme.md](InfraBD/Readme.md) # Instruções para inicializar o banco no Docker<br>
├── app/ # Pasta com o projeto Python<br>
│ ├── Util/ # Utilitários e módulos Python<br>
│ │ ├── bd.py # Arquivo Python com função para conectar no Banco de Dados<br>
│ │ └── paramsBD.yml # Arquivo com as configurações para conexão com o Banco de Dados<br>
│ ├── crudAlunos.py # Microserviço de CRUD de Alunos<br>
│ └── [Readme.md](app/Readme.md) # Instruções para inicializar o APP<br>
├── docker-compose.yml # Define a configuração para dois serviços: app e db<br>
├── Dockerfile # Define a configuração para construir uma imagem Docker para a aplicação Flask<br>
└── README.md # Arquivo com instruções gerais<br>

## Como Rodar o Docker-Compose

Para rodar o projeto utilizando o Docker-Compose, siga os passos abaixo:

1. Certifique-se de que você tem o Docker e o Docker-Compose instalados na sua máquina.

2. No diretório raiz do projeto, execute o seguinte comando para parar e remover quaisquer contêineres existentes:

    ```sh
    docker-compose down
    ```

3. Remova o volume de dados do PostgreSQL (se necessário):

    ```sh
    docker volume rm prj_escola_postgres_data
    ```

4. Execute o comando para iniciar os contêineres com o Docker-Compose:

    ```sh
    docker-compose up --build
    ```

5. O serviço Flask estará disponível em `http://localhost:5000` e o banco de dados PostgreSQL estará disponível na porta `5432`.

## Endpoints do Microserviço de Alunos

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

## Testes Automatizados

Para rodar os testes automatizados com `pytest`, execute:
```sh
pytest
```

Este README fornece uma visão geral do projeto e instruções detalhadas para configurar e executar o ambiente.