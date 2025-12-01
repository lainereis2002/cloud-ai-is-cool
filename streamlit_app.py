import streamlit as st
import requests
import os

# --- Configuração do Back-end FastAPI ---
# IMPORTANTE: Mude 'BACKEND_URL' para o URL do seu deploy no Render!
# Usamos uma variável de ambiente para que seja fácil mudar no deploy.
FASTAPI_BACKEND_URL = os.getenv("FASTAPI_BACKEND_URL", "http://127.0.0.1:8000") 
CHAT_ENDPOINT = f"{FASTAPI_BACKEND_URL}/chat"


# --- Funções do Chat ---

def get_chatbot_response(prompt: str):
    """Envia a pergunta do usuário para a API do FastAPI e retorna a resposta."""
    try:
        # Define o corpo da requisição JSON conforme o modelo Pydantic do seu FastAPI
        payload = {"message": prompt}
        
        # Faz a chamada POST para o seu endpoint /chat
        response = requests.post(CHAT_ENDPOINT, json=payload, timeout=30)
        response.raise_for_status() # Levanta um erro para códigos de status 4xx/5xx

        # Retorna a resposta formatada
        return response.json().get("response", "Erro: Resposta vazia da API.")

    except requests.exceptions.Timeout:
        return "Erro: A requisição expirou. A API do LLM está demorando muito."
    except requests.exceptions.RequestException as e:
        # Trata erros de conexão ou erros de status HTTP
        return f"Erro de conexão com o back-end: {e}"


# --- Interface Streamlit ---

st.set_page_config(
    page_title="Assistente de Estudos Cloud",
    layout="centered"
)
st.title("🤖 Assistente Inteligente de Estudos em Cloud")
st.caption("Desenvolvido com Python, FastAPI e Gemini API.")

# Inicializa o histórico do chat na session state do Streamlit
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Olá! Eu sou seu assistente em Cloud. Como posso ajudar em seus estudos de FastAPI ou Docker?"}
    ]

# Exibe o histórico de mensagens
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Captura a entrada do usuário
if prompt := st.chat_input("Pergunte-me algo sobre Cloud, FastAPI ou Docker..."):
    # 1. Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 2. Obtém a resposta do back-end (FastAPI)
    with st.spinner("Pensando..."):
        full_response = get_chatbot_response(prompt)
    
    # 3. Adiciona a resposta do assistente e a exibe
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.chat_message("assistant").write(full_response)