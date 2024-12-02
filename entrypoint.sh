#!/bin/sh

# Para a execução em caso de erro
set -e

# Executa as migrações do banco de dados
poetry run alembic upgrade head

# Inicia a aplicação
poetry run uvicorn --host 0.0.0.0 --port 8000 api.app:app
