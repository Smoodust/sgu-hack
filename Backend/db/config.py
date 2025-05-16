# PostgreSQL configuration
user = "postgres"
password = "data123"
host = "localhost"
port = "5432"
database = "sgu_hack"
token_proverka = '32631.OK3qCkZZqwnADnu8j'


# Команда для запуска контейнера
# docker run --name fintech-postgres \
#     -e POSTGRES_USER=postgres \
#     -e POSTGRES_PASSWORD=postgres \
#     -e POSTGRES_DB=fintech_db \
#     -p 5432:5432 \
#     -d postgres:latest