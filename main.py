from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Importa o módulo para a Gemini API
from google import genai
from google.genai.errors import APIError

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configuração Básica do FastAPI ---
app = FastAPI(
    title="Assistente Inteligente de Estudos (Chatbot LLM)",
    description="API para um chatbot educacional usando Python, FastAPI e Gemini API.",
    version="1.0.0"
)

# --- Modelo de Requisição (Schema Pydantic) ---
# Define como o corpo da requisição POST deve ser
class ChatRequest(BaseModel):
    # A mensagem do estudante para o chatbot
    message: str

# --- Inicialização da Gemini API ---
# A chave da API é lida da variável de ambiente GEMINI_API_KEY
# Garanta que esta variável esteja configurada no seu ambiente local e no serviço de deploy.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY não está configurada nas variáveis de ambiente.")

try:
    # Inicializa o cliente do Gemini
    client = genai.Client(api_key=GEMINI_API_KEY)
    # Escolha do modelo (gemini-2.5-flash é ótimo para performance e custo)
    MODEL = 'gemini-2.5-flash'
except Exception as e:
    # Trata erros de inicialização
    print(f"Erro ao inicializar o cliente Gemini: {e}")
    client = None

# --- Endpoints da API ---

# 1. Endpoint de Verificação de Saúde (Health Check)
@app.get("/", summary="Verifica se a API está online")
async def health_check():
    """Endpoint simples para verificar a saúde da API."""
    return {"status": "ok", "message": "Assistente de estudos online!"}

# 2. Endpoint Principal do Chatbot
@app.post("/chat", summary="Envia uma pergunta e recebe uma resposta do assistente")
async def process_chat(request: ChatRequest):
    """
    Recebe uma pergunta do estudante e usa um modelo de linguagem
    avançado (LLM) para gerar uma resposta de auxílio.
    """
    if client is None:
         # Erro se o cliente da API externa não foi inicializado
        raise HTTPException(
            status_code=503,
            detail="Serviço de LLM indisponível. Verifique a chave da API."
        )

    # --- Lógica de Negócio (Interação com o LLM) ---
    try:
        # Define a instrução (system instruction) para personalizar o chatbot
        # Isso é fundamental para que ele aja como um "Assistente inteligente que auxilia estudantes"
        system_instruction = (
            "Você é um assistente inteligente e amigável, especialista em Cloud, Python e FastAPI. "
            "Sua função é auxiliar estudantes em suas dúvidas de forma clara, didática e motivacional. "
            "Responda a pergunta a seguir de forma concisa e útil."
        )

        # Configuração da chamada do modelo
        config = genai.types.GenerateContentConfig(
            system_instruction=system_instruction
        )

        # Chama a API do Gemini para gerar a resposta
        response = client.models.generate_content(
            model=MODEL,
            contents=request.message,
            config=config
        )

        # Retorna a resposta gerada
        return {
            "query": request.message,
            "response": response.text,
            "model_used": MODEL
        }

    except APIError as e:
        # Trata erros da API externa
        raise HTTPException(
            status_code=500,
            detail=f"Erro na comunicação com a API do modelo de linguagem: {e}"
        )
    except Exception as e:
        # Trata outros erros inesperados
        raise HTTPException(
            status_code=500,
            detail=f"Ocorreu um erro interno: {e}"
        )

# --- Fim do main.py ---