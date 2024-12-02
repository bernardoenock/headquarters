#!/bin/bash

# Remove todos os diretórios __pycache__
find . -type d -name '__pycache__' -exec rm -r {} +

# Remove o ambiente virtual existente, se houver
if [ -d "venv" ]; then
    echo "Removing the existing virtual environment..."
    rm -rf venv
fi

# # Cria um novo ambiente virtual
# echo "Criando um novo ambiente virtual..."
# python3 -m venv venv

# # Ativa o ambiente virtual
# source venv/bin/activate

# # Instala as dependências
# echo "Instalando as dependências do requirements.txt..."
# pip install -r requirements.txt

# echo "Ambiente configurado com sucesso!"
