# 🤖 **Headquarters** 🤖  

![Agents and Bots in Action](https://media.giphy.com/media/l4pTfx2qLszoacZRS/giphy.gif)  

**Headquarters** é uma aplicação para iniciar bots e agentes de IA. Com suporte para FastAPI, gerencia automações de forma eficiente e estruturada.  

---

## 🚀 **Como Iniciar o Projeto**  

### **Com Poetry**  
1. **Criar o ambiente virtual**:  
   ```bash
   poetry env use 3.12
   ```  
2. **Instalar dependências**:  
   ```bash
   poetry install
   ```  
3. **Rodar comandos**:  
   ```bash
   poetry run <comando>
   ```  
4. **Ativar o ambiente virtual**:  
   ```bash
   poetry shell
   ```  

### **Com Venv**  
1. **Criar o venv**:  
   ```bash
   python3 -m venv .venv
   ```  
2. **Ativar o venv**:  
   ```bash
   source .venv/bin/activate
   ```  
3. **Desativar o venv**:  
   ```bash
   deactivate
   ```  

> **Dica:** Antes de abrir o VSCode, ative o venv. 🛠️  

---

## 🛠️ **Comandos Úteis**  

### **API em Desenvolvimento**  
```bash
poetry run fastapi dev api/app.py
```  

### **Lint e Formatação**  
- Verificar:  
  ```bash
  ruff check .
  ```  
- Corrigir:  
  ```bash
  ruff check . --fix
  ```  

### **Testes**  
- Rodar testes com cobertura:  
  ```bash
  pytest --cov=api
  coverage html
  ```  

### **Gerenciar Migrações**  
1. **Inicializar Alembic**:  
   ```bash
   alembic init migrations
   ```  
2. **Criar uma nova migração**:  
   ```bash
   alembic revision --autogenerate -m "create users table"
   ```  
3. **Aplicar migrações**:  
   ```bash
   alembic upgrade head
   ```  

---

## 🧪 **Estrutura de Testes**  

![Testing](https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif)  

Os testes seguem a estrutura:  
1. **Arrange**: Configurar o estado inicial.  
2. **Act**: Executar a ação a ser testada.  
3. **Assert**: Validar os resultados.  
4. **Teardown**: Limpar o ambiente após o teste.  

---

## 🗑️ **Limpando o Docker**  
Remova containers e imagens rapidamente:  
```bash
docker rm -f $(docker ps -a -q) && docker image rm -f $(docker image ls -a -q)
```  

---

## 🌐 **Túnel HTTP com Ngrok**  
Para expor a API localmente:  
```bash
ngrok http http://127.0.0.1:8000/
```  

---

## 📂 **Estrutura de Arquivos**  

```
📂 api_trigger/
├── api/
│   ├── app.py
│   ├── bots/
│   ├── control/
│   ├── migrations/
│   ├── pdf_output/
├── tests/
├── README.md
├── pyproject.toml
```  

---

## 🎉 **Recursos da API**  
1. **Ponto inicial**:  
   ```bash
   GET /
   ```  
   Resposta:  
   ```json
   { "message": "🤖 Headquarters started! 🤖" }
   ```  
2. **Página de exemplo**:  
   ```bash
   GET /pagex
   ```  
   Exibe:  
   ```html
   <h1>Agents & Bots</h1>
   ```  
3. **Servir PDFs**:  
   - Diretório de PDFs: `/pdfs`  
   - Buscar PDF específico: `/pdf/{pdf_name}`  

4. **Em um futuro proximo mais funcionalidades**
...

---

![Let's Code](https://media.giphy.com/media/ZVik7pBtu9dNS/giphy.gif)  

🎯 **Autor:** Enock  
Contribuições e melhorias são bem-vindas!