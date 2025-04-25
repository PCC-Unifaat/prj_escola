# Usar uma imagem base do Python
FROM python:3.9-slim

# Definir o diretório de trabalho no container
WORKDIR /

# Copiar os arquivos necessários para o container
COPY  /app/requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app .

# Comando para iniciar o microserviço
CMD ["python", "crudAlunos.py"]