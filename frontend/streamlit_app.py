import streamlit as st
import requests
import os
import json

# --- Configuração do Back-end FastAPI ---
FASTAPI_BACKEND_URL = os.getenv("FASTAPI_BACKEND_URL", "http://127.0.0.1:8000") 
CHAT_ENDPOINT = f"{FASTAPI_BACKEND_URL}/chat"

st.set_page_config(
    page_title="Assistente de Estudos Cloud",
    layout="centered"
)

# --- Funções do Chat ---

def get_chatbot_response(prompt: str):
    """Envia a pergunta do usuário para a API do FastAPI e retorna a resposta."""
    try:
        # Define o corpo da requisição JSON conforme o modelo Pydantic do seu FastAPI
        payload = {"message": prompt}
        
        st.write(f"📡 Connecting to: {CHAT_ENDPOINT}")
        
        # Faz a chamada POST para o seu endpoint /chat
        response = requests.post(
            CHAT_ENDPOINT, 
            json=payload, 
            timeout=60,
            headers={"Content-Type": "application/json"}
        )
        
        # Debug: mostra o status code
        st.write(f"Status Code: {response.status_code}")
        
        if response.status_code != 200:
            st.write(f"Full response: {response.text}")
        
        response.raise_for_status()  # Levanta um erro para códigos de status 4xx/5xx

        # Retorna a resposta formatada
        result = response.json()
        return result.get("response", "Error: Empty answer from API.")

    except requests.exceptions.Timeout:
        return "⏱️ Error: The request timed out. The LLM API is taking too long."
    except requests.exceptions.ConnectionError:
        return f"❌ Connection error: Could not connect to the API at {CHAT_ENDPOINT}. Check if the FastAPI server is running."
    except requests.exceptions.HTTPError as e:
        try:
            error_detail = e.response.json().get("detail", str(e))
        except:
            error_detail = str(e)
        return f"❌ HTTP Error {e.response.status_code}: {error_detail}"
    except requests.exceptions.RequestException as e:
        return f"❌ Connection error with the back-end.: {e}"
    except json.JSONDecodeError:
        return "❌ Error: The API response is not valid JSON."
    except Exception as e:
        return f"❌ Unexpected error: {type(e).__name__}: {e}"


# --- Interface Streamlit ---

st.title("🤖 BeeMo - Artificial Inteligence")
st.caption("You can aske me anything, I'll help you. Develop with Python, FastAPI and Gemini API.")

# Mostra URL de debug
with st.expander("🔧 Debug Configuration"):
    st.write(f"**Backend URL:** {FASTAPI_BACKEND_URL}")
    st.write(f"**Chat Endpoint:** {CHAT_ENDPOINT}")
    
    # Testa conexão
    if st.button("Connection Test"):
        try:
            test_response = requests.get(f"{FASTAPI_BACKEND_URL}/", timeout=5)
            if test_response.status_code == 200:
                st.success("✅ Beckend connection stablished!")
                st.write(test_response.json())
            else:
                st.error(f"❌ Status code: {test_response.status_code}")
        except Exception as e:
            st.error(f"❌ Connection Error: {e}")

# Inicializa o histórico do chat na session state do Streamlit
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi! I'm BeeMo, your AI personal helper. How can I help you?"}
    ]

# Exibe o histórico de mensagens
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Captura a entrada do usuário
if prompt := st.chat_input("Ask me something..."):
    # 1. Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 2. Obtém a resposta do back-end (FastAPI)
    with st.spinner("⏳ Hm...Let me think..."):
        full_response = get_chatbot_response(prompt)
    
    # 3. Adiciona a resposta do assistente e a exibe
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.chat_message("assistant").write(full_response)