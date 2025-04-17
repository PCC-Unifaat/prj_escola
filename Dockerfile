# Usar uma imagem base do Python
FROM python:3.9-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos necessários para o container
COPY app/ /app/
COPY app/Util/paramsBD.yml /app/Util/paramsBD.yml

# Instalar as dependências                                                                                                                                                      
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expor a porta que o Flask usará
EXPOSE 5000

# Comando para iniciar o microserviço
CMD ["python", "crudAlunos.py"]