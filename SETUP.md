# 🚀 Assistente Inteligente de Estudos em Cloud

Sistema de chatbot educacional usando Python, FastAPI e Gemini API.

## 📋 Pré-requisitos

- Python 3.9+
- pip
- Variável de ambiente `GEMINI_API_KEY` configurada

## 🔧 Instalação

### 1. Clone o repositório
```bash
git clone <seu-repo>
cd cloud-ai-is-cool
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
cd frontend
pip install -r requirements.txt
cd ..
```

### 4. Configure variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```
GEMINI_API_KEY=sua-chave-de-api-aqui
FASTAPI_BACKEND_URL=http://127.0.0.1:8000
```

## 🎯 Como rodar

### Terminal 1: Inicie o servidor FastAPI
```bash
uvicorn main:app --reload
```

O servidor estará disponível em: `http://127.0.0.1:8000`

### Terminal 2: Inicie a aplicação Streamlit
```bash
cd frontend
streamlit run streamlit_app.py
```

A aplicação abrirá automaticamente em: `http://localhost:8501`

## 🧪 Testando a API

Se quiser testar a API sem usar o Streamlit:

```bash
python test_api.py
```

Ou teste manualmente com curl:

```bash
# Health check
curl http://127.0.0.1:8000/

# Chat
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá, como você funciona?"}'
```

## 📁 Estrutura do Projeto

```
.
├── main.py                 # API FastAPI principal
├── teste.py                # Script de teste básico
├── test_api.py             # Script de teste completo
├── requirements.txt        # Dependências do backend
├── .env                    # Variáveis de ambiente
├── Dockerfile              # Configuração Docker
└── frontend/
    ├── streamlit_app.py    # Interface Streamlit
    └── requirements.txt    # Dependências do frontend
```

## 🐛 Troubleshooting

### Erro: "GEMINI_API_KEY não está configurada"
- Certifique-se de criar o arquivo `.env`
- Verifique se a chave está correta

### Erro: "Method Not Allowed"
- Isso geralmente é um problema de CORS
- O código foi atualizado com suporte completo a CORS
- Reinicie o servidor FastAPI

### Erro: "Connection refused"
- Verifique se o servidor FastAPI está rodando
- Execute: `uvicorn main:app --reload` em outro terminal

### Erro: "Timeout"
- A API Gemini está demorando muito
- Aguarde alguns segundos e tente novamente
- Verifique seu plano de cota

## 📚 Endpoints da API

### GET /
Health check da API.

**Resposta:**
```json
{
  "status": "ok",
  "message": "Assistente de estudos online!"
}
```

### POST /chat
Envia uma pergunta e recebe uma resposta.

**Request:**
```json
{
  "message": "Sua pergunta aqui"
}
```

**Response:**
```json
{
  "query": "Sua pergunta aqui",
  "response": "Resposta do assistente",
  "model_used": "gemini-2.5-flash"
}
```

### GET /debug/config
Verifica a configuração do sistema (apenas debug).

**Resposta:**
```json
{
  "gemini_api_key_configured": true,
  "model": "gemini-2.5-flash",
  "client_initialized": true
}
```

## 🚀 Deploy

Para fazer deploy:

1. Configure as variáveis de ambiente no seu serviço de hosting
2. Certifique-se de que a `GEMINI_API_KEY` está configurada
3. Atualize `FASTAPI_BACKEND_URL` no Streamlit se necessário

## 📝 Licença

MIT
