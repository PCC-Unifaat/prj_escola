# app/Dockerfile

FROM python:3.10

# Define diretório de trabalho no container
WORKDIR /app

# Copia os arquivos da pasta app para o container
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta do Flask
EXPOSE 5000

# Comando para iniciar o app com o servidor Flask
CMD ["python", "crudAlunos.py"]
