# Use uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
# WORKDIR /app

# Copia os arquivos de requisitos para o container
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o container
COPY . .

# Expõe a porta que a API usará
EXPOSE 5000

# Define o comando para iniciar a aplicação
CMD ["python", "crudAlunos.py"]