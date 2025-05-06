-- Criação do banco de dados
--CREATE DATABASE IF NOT EXISTS escola;
--USE escola;

-- Tabela professor
CREATE TABLE IF NOT EXISTS professor (
    id_professor SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255),
    email VARCHAR(100),
    telefone VARCHAR(20)
);

-- Tabela turma
CREATE TABLE IF NOT EXISTS turma (
    id_turma SERIAL PRIMARY KEY,
    nome_turma VARCHAR(50),
    id_professor INT,
    horario VARCHAR(100),
    FOREIGN KEY (id_professor) REFERENCES professor(id_professor)
);

-- Tabela aluno
CREATE TABLE IF NOT EXISTS aluno (
    id_aluno SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255),
    data_nascimento DATE,
    id_turma INT,
    nome_responsavel VARCHAR(255),
    telefone_responsavel VARCHAR(20),
    email_responsavel VARCHAR(100),
    informacoes_adicionais TEXT,
    FOREIGN KEY (id_turma) REFERENCES turma(id_turma)
);

-- Tabela pagamento
CREATE TABLE IF NOT EXISTS pagamento (
    id_pagamento SERIAL PRIMARY KEY,
    id_aluno INT,
    data_pagamento DATE,
    valor_pago DECIMAL(10, 2),
    forma_pagamento VARCHAR(50),
    referencia VARCHAR(100),
    status VARCHAR(20),
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno)
);

-- Tabela presenca
CREATE TABLE IF NOT EXISTS presenca (
    id_presenca SERIAL PRIMARY KEY,
    id_aluno INT,
    data_presenca DATE,
    presente BOOLEAN,
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno)
);

-- Tabela atividade
CREATE TABLE IF NOT EXISTS atividade (
    id_atividade SERIAL PRIMARY KEY,
    descricao TEXT,
    data_realizacao DATE
);

-- Tabela de ligação atividade_aluno
CREATE TABLE IF NOT EXISTS atividade_aluno (
    id_atividade INT,
    id_aluno INT,
    PRIMARY KEY (id_atividade, id_aluno),
    FOREIGN KEY (id_atividade) REFERENCES atividade(id_atividade),
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno)
);

-- Tabela usuario
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE,
    senha VARCHAR(255),
    nivel_acesso VARCHAR(20),
    id_professor INT,
    FOREIGN KEY (id_professor) REFERENCES professor(id_professor)
);