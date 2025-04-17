# Utiliza a imagem oficial mais recente do PostgreSQL como base.
FROM postgres:13

# Defina variáveis de ambiente para configurar o PostgreSQL
ENV POSTGRES_DB=escola
ENV POSTGRES_USER=faat
ENV POSTGRES_PASSWORD=faat

# Copie o script de inicialização para o diretório de inicialização do PostgreSQL
COPY escola.sql /docker-entrypoint-initdb.d/

# Exponha a porta padrão do PostgreSQL
EXPOSE 5432