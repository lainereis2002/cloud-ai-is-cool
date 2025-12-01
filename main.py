from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging

# Importa o módulo para a Gemini API
from google import genai
from google.genai.errors import APIError

# --- Configuração de Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configuração Básica do FastAPI ---
app = FastAPI(
    title="Assistente Inteligente de Estudos (Chatbot LLM)",
    description="API para um chatbot educacional usando Python, FastAPI e Gemini API.",
    version="1.0.0"
)

# --- Configuração de CORS ---
# Permite que o Streamlit se comunique com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, mude para específico: ["https://seu-dominio.com"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# --- Modelo de Requisição (Schema Pydantic) ---
# Define como o corpo da requisição POST deve ser
class ChatRequest(BaseModel):
    # A mensagem do estudante para o chatbot
    message: str

# --- Inicialização da Gemini API ---
# A chave da API é lida da variável de ambiente GEMINI_API_KEY
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    logger.error("GEMINI_API_KEY não está configurada nas variáveis de ambiente.")
    raise ValueError("GEMINI_API_KEY não está configurada nas variáveis de ambiente.")

try:
    # Inicializa o cliente do Gemini
    client = genai.Client(api_key=GEMINI_API_KEY)
    # Escolha do modelo
    MODEL = 'gemini-2.5-flash'
    logger.info(f"Cliente Gemini inicializado com sucesso. Modelo: {MODEL}")
except Exception as e:
    # Trata erros de inicialização
    logger.error(f"Erro ao inicializar o cliente Gemini: {e}")
    client = None

# --- Endpoints da API ---

# 1. Endpoint de Verificação de Saúde (Health Check)
@app.get("/", summary="Verifica se a API está online")
async def health_check():
    """Endpoint simples para verificar a saúde da API."""
    logger.info("Health check realizado")
    return {"status": "ok", "message": "Assistente de estudos online!"}

# 2. Endpoint Principal do Chatbot
@app.post("/chat", summary="Envia uma pergunta e recebe uma resposta do assistente")
async def process_chat(request: ChatRequest):
    """
    Recebe a pergunta do estudante e usa o LLM para gerar uma resposta.
    """
    logger.info(f"Requisição de chat recebida: {request.message[:50]}...")
    
    if client is None:
        logger.error("Cliente Gemini não foi inicializado corretamente")
        raise HTTPException(
            status_code=503,
            detail="Serviço de LLM indisponível. Verifique a chave da API."
        )

    # --- Lógica de Negócio (Interação com o LLM) ---
    try:
        # Personalização (System Instruction)
        system_instruction = (
            "Você é um assistente inteligente e amigável, especialista em Cloud, Python e FastAPI. "
            "Sua função é auxiliar estudantes em suas dúvidas de forma clara, didática e motivacional. "
            "Responda a pergunta a seguir de forma concisa e útil."
        )

        logger.info(f"Enviando requisição para o modelo {MODEL}")
        
        # Chamada para a API Gemini com configuração
        config = genai.types.GenerateContentConfig(
            system_instruction=system_instruction
        )
        
        response = client.models.generate_content(
            model=MODEL,
            contents=request.message,
            config=config
        )

        logger.info("Resposta recebida com sucesso")
        
        # Retorna a resposta gerada
        return {
            "query": request.message,
            "response": response.text,
            "model_used": MODEL
        }

    except APIError as e:
        # Trata erros da API Gemini
        error_message = str(e)
        logger.error(f"APIError da Gemini: {error_message}")
        
        if "RESOURCE_EXHAUSTED" in error_message:
            raise HTTPException(
                status_code=429,
                detail="Cota de uso da API Gemini excedida. Por favor, aguarde ou verifique seu plano."
            )
        elif "INVALID_ARGUMENT" in error_message:
            raise HTTPException(
                status_code=400,
                detail=f"Argumento inválido na requisição: {error_message}"
            )
        elif "NOT_FOUND" in error_message:
            raise HTTPException(
                status_code=404,
                detail=f"Modelo não encontrado: {error_message}"
            )
        elif "PERMISSION_DENIED" in error_message:
            raise HTTPException(
                status_code=403,
                detail=f"Permissão negada - Verifique sua chave de API: {error_message}"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Erro na comunicação com a API do modelo de linguagem: {error_message}"
            )
            
    except Exception as e:
        # Trata outros erros inesperados
        logger.error(f"Erro inesperado: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Ocorreu um erro interno: {str(e)}"
        )

# --- Endpoint para debug ---
@app.get("/debug/config", summary="Verifica a configuração do sistema (apenas para debug)")
async def debug_config():
    """Endpoint de debug para verificar se tudo está configurado corretamente."""
    return {
        "gemini_api_key_configured": GEMINI_API_KEY is not None,
        "model": MODEL if client else "Não configurado",
        "client_initialized": client is not None,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)