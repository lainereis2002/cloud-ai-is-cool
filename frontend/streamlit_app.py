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
        
        st.write(f"📡 Conectando a: {CHAT_ENDPOINT}")
        
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
            st.write(f"Resposta completa: {response.text}")
        
        response.raise_for_status()  # Levanta um erro para códigos de status 4xx/5xx

        # Retorna a resposta formatada
        result = response.json()
        return result.get("response", "Erro: Resposta vazia da API.")

    except requests.exceptions.Timeout:
        return "⏱️ Erro: A requisição expirou. A API do LLM está demorando muito."
    except requests.exceptions.ConnectionError:
        return f"❌ Erro de conexão: Não foi possível conectar à API em {CHAT_ENDPOINT}. Verifique se o servidor FastAPI está rodando."
    except requests.exceptions.HTTPError as e:
        try:
            error_detail = e.response.json().get("detail", str(e))
        except:
            error_detail = str(e)
        return f"❌ Erro HTTP {e.response.status_code}: {error_detail}"
    except requests.exceptions.RequestException as e:
        return f"❌ Erro de conexão com o back-end: {e}"
    except json.JSONDecodeError:
        return "❌ Erro: A resposta da API não é um JSON válido."
    except Exception as e:
        return f"❌ Erro inesperado: {type(e).__name__}: {e}"


# --- Interface Streamlit ---

st.title("🤖 Assistente Inteligente de Estudos em Cloud")
st.caption("Desenvolvido com Python, FastAPI e Gemini API.")

# Mostra URL de debug
with st.expander("🔧 Configurações de Debug"):
    st.write(f"**URL do Backend:** {FASTAPI_BACKEND_URL}")
    st.write(f"**Endpoint do Chat:** {CHAT_ENDPOINT}")
    
    # Testa conexão
    if st.button("Testar Conexão"):
        try:
            test_response = requests.get(f"{FASTAPI_BACKEND_URL}/", timeout=5)
            if test_response.status_code == 200:
                st.success("✅ Conexão com o backend bem-sucedida!")
                st.write(test_response.json())
            else:
                st.error(f"❌ Status code: {test_response.status_code}")
        except Exception as e:
            st.error(f"❌ Erro ao conectar: {e}")

# Inicializa o histórico do chat na session state do Streamlit
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Olá! Eu sou seu assistente em Cloud. Como posso ajudar em seus estudos?"}
    ]

# Exibe o histórico de mensagens
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Captura a entrada do usuário
if prompt := st.chat_input("Pergunte-me algo..."):
    # 1. Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 2. Obtém a resposta do back-end (FastAPI)
    with st.spinner("⏳ Pensando..."):
        full_response = get_chatbot_response(prompt)
    
    # 3. Adiciona a resposta do assistente e a exibe
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.chat_message("assistant").write(full_response)