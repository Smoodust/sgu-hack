# PostgreSQL configuration
user = "postgres"
password = "data123"
host = "postgres_fast_api"
port = "5432"
database = "sgu_hack"
token_proverka = '32631.OK3qCkZZqwnADnu8j'

URL_PARSE_LOGS = 'https://rdb.altlinux.org/api/export/beehive/ftbfs?branch=sisyphus&arch=x86_64'

# Команда для запуска контейнера
# docker run --name sgu-hack-postgres \
#     -e POSTGRES_USER=postgres \
#     -e POSTGRES_PASSWORD=data123 \
#     -e POSTGRES_DB=sgu_hack \
#     -p 5432:5432 \
#     -d postgres:latest