import pytest
from app.crudAlunos import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_listar_alunos(client):
    response = client.get('/alunos')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_cadastrar_aluno(client):
    novo_aluno = {
        "aluno_id": "123",
        "nome_completo": "João Silva",
        "data_nascimento": "2000-01-01",
        "id_turma": "1",
        "nome_responsavel": "Maria Silva",
        "telefone_responsavel": "123456789",
        "email_responsavel": "maria@example.com",
        "informacoes_adicionais": "Nenhuma"
    }
    response = client.post('/alunos', json=novo_aluno)
    assert response.status_code == 201
    assert response.json["message"] == "Aluno cadastrado com sucesso"

def test_atualizar_aluno(client):
    aluno_atualizado = {
        "nome_completo": "João Silva Atualizado",
        "data_nascimento": "2000-01-01",
        "id_turma": "1",
        "nome_responsavel": "Maria Silva",
        "telefone_responsavel": "987654321",
        "email_responsavel": "maria@example.com",
        "informacoes_adicionais": "Atualizado"
    }
    response = client.put('/alunos/123', json=aluno_atualizado)
    assert response.status_code == 200
    assert response.json["message"] == "Aluno atualizado com sucesso"

def test_deletar_aluno(client):
    response = client.delete('/alunos/123')
    assert response.status_code == 200
    assert response.json["message"] == "Aluno deletado com sucesso"