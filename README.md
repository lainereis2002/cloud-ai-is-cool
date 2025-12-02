# 🤖 BeeMo - AI Assistant

> Um sistema de chatbot educacional inteligente que utiliza a Gemini API do Google para responder dúvidas de forma clara, didática e motivacional.

**Repositório dedicado para segunda avaliação da disciplina de Cloud.**

---

## 📚 Tabela de Conteúdos

1. [O que é?](#1-o-que-é)
2. [Como Rodar](#2-como-rodar)
3. [Design Pattern](#3-design-pattern)
4. [Containerização com Render](#4-containerização-com-render)

---

## 1️⃣ O que é?

### Visão Geral

O **Assistente Inteligente** é uma aplicação full-stack que combina:

- **Backend**: API REST construída com **FastAPI** (Python)
- **Frontend**: Interface interativa com **Streamlit** (Python)
- **LLM**: Gemini 2.5 Flash do Google para gerar respostas inteligentes

### Funcionalidades Principais

✅ **Chat em Tempo Real** - Interação fluida entre usuário e assistente  
✅ **Respostas Personalizadas** - System instructions customizadas para educação  
✅ **CORS Habilitado** - Comunicação entre frontend e backend sem restrições  
✅ **Tratamento Robusto de Erros** - Feedback claro ao usuário  
✅ **Health Check** - Verificação da saúde da API  
✅ **Logging Detalhado** - Debug facilitado em produção  

### Arquitetura

```
┌─────────────────────────────────────────────────────┐
│                    Frontend (Streamlit)             │
│              Interface Web Interativa                │
│           (http://localhost:8501)                   │
└────────────────────┬────────────────────────────────┘
                     │
                HTTP POST /chat
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              Backend (FastAPI)                      │
│          API REST (http://localhost:8000)          │
│    - Health Check: GET /                           │
│    - Chat: POST /chat                              │
│    - Debug: GET /debug/config                      │
└────────────────────┬────────────────────────────────┘
                     │
              API Gemini v1beta
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│         Google Gemini API (LLM)                     │
│      Processamento de Linguagem Natural             │
└─────────────────────────────────────────────────────┘
```

### Stack Tecnológico

| Componente | Tecnologia | Versão |
|-----------|-----------|--------|
| **Runtime** | Python | 3.9+ |
| **Backend** | FastAPI | 0.123.0+ |
| **Frontend** | Streamlit | 1.28.0+ |
| **LLM** | google-genai | 1.47.0+ |
| **Server** | Uvicorn | 0.23.0+ |
| **CORS** | fastapi.middleware | Integrado |
| **Environment** | python-dotenv | 1.0.0+ |

---

## 2️⃣ Como Rodar

### Pré-requisitos

- **Python 3.9+** instalado
- **pip** para gerenciamento de pacotes
- **Chave de API do Google Gemini** (gratuita em [AI Studio](https://aistudio.google.com/))
- **Git** (opcional, para clonar o repositório)

### Instalação Local

#### Passo 1: Clone o repositório
```bash
git clone https://github.com/lainereis2002/cloud-ai-is-cool.git
cd cloud-ai-is-cool
```

#### Passo 2: Crie um ambiente virtual
```bash
python -m venv venv

# Ative o ambiente virtual
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate     # Windows
```

#### Passo 3: Instale as dependências

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend (em outro terminal):**
```bash
cd frontend
pip install -r requirements.txt
cd ..
```

#### Passo 4: Configure variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:
```env
GEMINI_API_KEY=sua-chave-de-api-aqui
FASTAPI_BACKEND_URL=http://127.0.0.1:8000
```

#### Passo 5: Execute a aplicação

**Terminal 1 - Backend (FastAPI):**
```bash
source venv/bin/activate  # ou venv\Scripts\activate no Windows
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Saída esperada:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:main:Cliente Gemini inicializado com sucesso. Modelo: gemini-2.5-flash
INFO:     Application startup complete.
```

**Terminal 2 - Frontend (Streamlit):**
```bash
source venv/bin/activate  # ou venv\Scripts\activate no Windows
cd frontend
streamlit run streamlit_app.py
```

A aplicação abrirá automaticamente em: **http://localhost:8501**

### Testando a API

#### Usando o Script de Teste:
```bash
python test_api.py
```

#### Usando cURL:
```bash
# Health Check
curl http://127.0.0.1:8000/

# Chat
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "O que é Cloud Computing?"}'

# Debug Config
curl http://127.0.0.1:8000/debug/config
```

#### Usando Python:
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/chat",
    json={"message": "Explique Python em uma frase"}
)

print(response.json())
```

### Troubleshooting

| Erro | Solução |
|------|---------|
| `GEMINI_API_KEY não está configurada` | Crie `.env` com a chave da API Gemini |
| `Address already in use :8000` | Mude a porta: `--port 8001` ou mate o processo: `lsof -ti:8000 \| xargs kill -9` |
| `Connection refused` | Verifique se FastAPI está rodando no Terminal 1 |
| `Timeout na requisição` | Aumente o timeout ou verifique sua cota Gemini |

---

## 3️⃣ Design Pattern

### Padrões de Design Implementados

#### 🏗️ **1. MVC (Model-View-Controller)**

```
Model (Pydantic)        View (Streamlit)        Controller (FastAPI)
    ↓                        ↓                          ↓
ChatRequest         UI Interativa          Endpoints REST
Schema JSON         Chat History           Lógica Business
Validação           Componentes            Orquestração
```

**Estrutura:**
- **Model**: `ChatRequest` (Pydantic BaseModel) valida entrada do usuário
- **View**: `streamlit_app.py` renderiza interface web
- **Controller**: `main.py` processa requisições e coordena lógica

#### 🔌 **2. Repository Pattern (Separação de Responsabilidades)**

```
Client (Streamlit)
       ↓
APIRepository (requests.post)
       ↓
FastAPI Endpoint (@app.post)
       ↓
LLMService (Google Gemini)
```

Cada camada tem responsabilidade clara:
- **Client Layer**: UI/Interação com usuário
- **API Layer**: Comunicação HTTP
- **Service Layer**: Lógica de negócio
- **LLM Layer**: Integração externa

#### 🛡️ **3. Middleware Pattern**

```python
app.add_middleware(
    CORSMiddleware,  # Permite comunicação Frontend ↔ Backend
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"]
)
```

Middleware aplicado para:
- ✅ Habilitar CORS
- ✅ Permitir requisições pré-voo (OPTIONS)
- ✅ Validar headers

#### 📝 **4. Adapter Pattern (LLM Integration)**

```python
# Interface unificada para diferentes modelos
class LLMAdapter:
    def generate_response(self, prompt: str) -> str:
        # Pode trocar Gemini por GPT, Claude, etc.
        pass
```

Permite trocar provedores LLM facilmente:
```python
# Hoje: Google Gemini
response = client.models.generate_content(...)

# Amanhã: OpenAI GPT
response = openai.ChatCompletion.create(...)
```

#### 🔄 **5. Singleton Pattern (Client Initialization)**

```python
# Instância única do cliente Gemini
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL = 'gemini-2.5-flash'

# Reutilizada em todas as requisições
@app.post("/chat")
async def process_chat(request: ChatRequest):
    response = client.models.generate_content(...)
```

Uma única instância do cliente em toda aplicação ✨

#### 🎯 **6. Observer Pattern (Error Handling)**

```python
try:
    response = client.models.generate_content(...)
except APIError as e:
    # Observer: Monitora erro específico
    if "RESOURCE_EXHAUSTED" in str(e):
        raise HTTPException(status_code=429)
except Exception as e:
    # Observer: Monitora erro genérico
    raise HTTPException(status_code=500)
```

Diferentes observadores reagem a diferentes erros

### Fluxo de Dados

```
1. Usuário digita pergunta no Streamlit
         ↓
2. Streamlit envia POST /chat com {"message": "..."}
         ↓
3. FastAPI recebe e valida com ChatRequest (Pydantic)
         ↓
4. Sistema instructions personalizado é aplicado
         ↓
5. API Gemini é chamada com conteúdo + config
         ↓
6. Resposta é formatada em JSON
         ↓
7. Streamlit renderiza resposta no chat
         ↓
8. Histórico é mantido no session_state do Streamlit
```

### Camadas de Abstração

```
┌─────────────────────────────────────────┐
│  Presentation Layer (Streamlit UI)      │
├─────────────────────────────────────────┤
│  Application Layer (FastAPI Routes)     │
├─────────────────────────────────────────┤
│  Business Logic Layer (Chat Processing) │
├─────────────────────────────────────────┤
│  Integration Layer (Gemini API Client)  │
├─────────────────────────────────────────┤
│  External Service (Google Gemini API)   │
└─────────────────────────────────────────┘
```

---

## 4️⃣ Containerização com Render

### O que é Render?

**Render** é uma plataforma cloud moderna que simplifica o deploy de aplicações. É a alternativa atualizada ao Heroku.

### Arquitetura Docker

Utilizamos **Multi-stage Build** para otimizar a imagem:

```dockerfile
# STAGE 1: Build
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# STAGE 2: Runtime (imagem final, mais leve)
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
EXPOSE 80
CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

**Benefícios:**
- ✅ Imagem final **50% mais leve** (builder layers são descartadas)
- ✅ Dependências instaladas uma só vez
- ✅ Melhor desempenho no deploy
- ✅ Menos uso de banda de rede

### Deploy no Render - Passo a Passo

#### 1️⃣ **Prepare o repositório**

Certifique-se que na raiz tem:
```
cloud-ai-is-cool/
├── Dockerfile           ✅ Multi-stage build
├── requirements.txt     ✅ Dependências backend
├── main.py             ✅ FastAPI app
├── .dockerignore        ✅ (opcional) excluir venv/, .git/
└── .env.example        ✅ (opcional) template de env
```

**Crie `.dockerignore` na raiz:**
```
venv/
.git/
.gitignore
__pycache__/
*.pyc
.env
.pytest_cache/
```

#### 2️⃣ **Configure environment no Render**

No painel do Render, configure as variáveis:

| Variável | Valor | Exemplo |
|----------|-------|---------|
| `GEMINI_API_KEY` | Sua chave | `AIzaSyA5JmXW...` |
| `FASTAPI_BACKEND_URL` | URL da API | `https://seu-app.onrender.com` |
| `PORT` | Porta (opcional) | `80` |

#### 3️⃣ **Deploy via Git**

```bash
# Push para GitHub/GitLab/Bitbucket
git add .
git commit -m "Deploy para Render"
git push origin main  # ou sua branch
```

#### 4️⃣ **Crie Web Service no Render**

1. Acesse https://dashboard.render.com
2. Clique em **"New +" → "Web Service"**
3. Conecte seu repositório Git
4. Configure:
   - **Name**: `cloud-ai-chatbot`
   - **Environment**: `Docker`
   - **Region**: `Ohio` (US) ou próximo
   - **Plan**: `Free` (trial) ou `Pay-as-you-go`

5. Clique em **"Deploy"**

#### 5️⃣ **Configure Variáveis de Ambiente**

No Render Dashboard:
1. Vá para **Settings → Environment**
2. Adicione as variáveis:
   ```
   GEMINI_API_KEY=sua-chave-aqui
   FASTAPI_BACKEND_URL=https://seu-app.onrender.com
   ```
3. Clique em **"Save"**

#### 6️⃣ **Deploy Manual (Opcional)**

Se a build falhar, redeploy:
```bash
# No dashboard, clique em "Manual Deploy → Deploy latest commit"
```

### Monitoramento no Render

#### Logs da Aplicação

```bash
# No dashboard, vá para "Logs"
# Você verá em tempo real:

INFO:     Uvicorn running on http://0.0.0.0:80
INFO:main:Cliente Gemini inicializado com sucesso
INFO:     Application startup complete
INFO:main:Requisição de chat recebida
```

#### Health Checks

Render faz checks automáticos:

```
GET https://seu-app.onrender.com/
Resposta esperada: {"status":"ok","message":"Assistente de estudos online!"}
```

Se falhar consecutivamente, a app fica em "red" (erro).

### URL Produção

Após deploy bem-sucedido:

- **Backend API**: `https://seu-app.onrender.com`
- **Health Check**: `https://seu-app.onrender.com/`
- **Chat Endpoint**: `https://seu-app.onrender.com/chat`

### Deploy do Frontend (Streamlit) no Render

#### Método 1: Usar Community Cloud (Grátis)

1. Commit seu código: `git push`
2. Acesse https://share.streamlit.io
3. Conecte seu repositório GitHub
4. Aponte para `frontend/streamlit_app.py`
5. Streamlit faz o deploy automaticamente

URL: `https://seu-username-cloud-ai-cool-xxxxx.streamlit.app`

#### Método 2: Web Service Separado (Pago)

1. Crie um `Dockerfile.streamlit` adicional
2. Deploy como outro Web Service no Render
3. Configure `FASTAPI_BACKEND_URL` apontando para seu backend

### Troubleshooting Deploy

| Erro | Solução |
|------|---------|
| `Build failed: pip install` | Atualize `requirements.txt`: `pip freeze > requirements.txt` |
| `GEMINI_API_KEY not found` | Verifique variável de ambiente no Render Settings |
| `Connection timeout` | Backend pode estar no plano free e ficou dormindo (cold start) |
| `Port already in use` | Dockerfile usa `--port 80`, não mude |

### Estrutura Completa do Deploy

```
GitHub Repository
    ↓
Render Webhook (automático ao push)
    ↓
Build Stage 1: Download código
    ↓
Build Stage 2: Multi-stage Docker build
    ↓
Build Stage 3: Docker push para registro Render
    ↓
Deploy: Container inicia
    ↓
Health Check: GET / passa? ✅
    ↓
App Online 🎉
    ↓
Streamlit Community Cloud (frontend)
    ↓
Usuários finais acessam:
https://seu-app.onrender.com (API)
https://seu-username-app.streamlit.app (UI)
```

### Exemplo `.env.example` para Render

Crie este arquivo na raiz para documentação:

```env
# Google Gemini API
GEMINI_API_KEY=key

# URLs da Aplicação
FASTAPI_BACKEND_URL=https://seu-app.onrender.com
STREAMLIT_SERVER_PORT=80

# FastAPI Config
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=80
```

---

## 📊 Resumo Executivo

| Aspecto | Descrição |
|--------|----------|
| **O que é?** | Assistente com IA (Gemini) que responde dúvidas |
| **Como rodar?** | `uvicorn main:app --reload` + `streamlit run streamlit_app.py` |
| **Padrões** | MVC, Repository, Middleware, Adapter, Singleton, Observer |
| **Deploy** | Docker multi-stage + Render Web Service |
| **Resultado** | App escalável, robusta e pronta para produção |

---

**Desenvolvido com ❤️ para a disciplina de Cloud Computing**

