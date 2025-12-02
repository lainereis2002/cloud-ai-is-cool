import streamlit as st
import requests
import os
import json

# --- Configuração do Back-end FastAPI ---
# A URL do Render/FastAPI. Lê da variável de ambiente ou usa o local como fallback.
FASTAPI_BACKEND_URL = os.getenv("FASTAPI_BACKEND_URL", "http://127.0.0.1:8000") 
CHAT_ENDPOINT = f"{FASTAPI_BACKEND_URL}/chat"

# --- Configuração da Página ---
st.set_page_config(
    page_title="Assistente de Estudos Cloud",
    layout="wide" # layout wide é ideal para usar a sidebar
)

# ----------------------------------------------------------------------
# FUNÇÕES DE CHAT
# ----------------------------------------------------------------------

def get_chatbot_response(prompt: str):
    """Envia a pergunta do usuário para a API do FastAPI e retorna a resposta."""
    try:
        payload = {"message": prompt}
        
        # Faz a chamada POST para o seu endpoint /chat
        response = requests.post(
            CHAT_ENDPOINT, 
            json=payload, 
            timeout=60,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status() # Levanta erro para 4xx/5xx

        # Retorna a resposta formatada
        result = response.json()
        return result.get("response", "Error: Empty answer from API.")

    # Tratamento de Erros Robusto (Mantido do seu código original)
    except requests.exceptions.Timeout:
        return "⏱️ Erro: A requisição expirou. A API do LLM está demorando muito."
    except requests.exceptions.ConnectionError:
        return f"❌ Erro de conexão: Não foi possível conectar à API em {CHAT_ENDPOINT}. Verifique se o FastAPI está rodando."
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

# ----------------------------------------------------------------------
# GERENCIAMENTO DE ESTADO E SIDEBAR
# ----------------------------------------------------------------------

def initialize_session_state():
    """Inicializa as conversas e o chat_atual na sessão."""
    if 'conversations' not in st.session_state:
        # Dicionário onde a chave é o nome do chat, e o valor é o histórico
        st.session_state['conversations'] = {
            "Chat 1": [{"role": "assistant", "content": "Olá! Eu sou BeeMo, seu ajudante especialista em Cloud Computing, Python e FastAPI. Como posso te ajudar?"}]
        }
    if 'current_chat' not in st.session_state:
        st.session_state['current_chat'] = "Chat 1"

def new_chat():
    """Cria uma nova conversa e a define como a conversa atual."""
    existing_keys = st.session_state['conversations'].keys()
    new_chat_index = 1
    while f"Chat {new_chat_index}" in existing_keys:
        new_chat_index += 1
    
    new_chat_name = f"Chat {new_chat_index}"
    
    st.session_state['conversations'][new_chat_name] = [
        {"role": "assistant", "content": f"Esta é uma nova conversa com o BeeMo ({new_chat_name}). Como eu posso te ajudar?"}
    ]
    st.session_state['current_chat'] = new_chat_name
    st.rerun() # Força a interface a atualizar para o novo chat

# Inicializa o estado
initialize_session_state()

# ----------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------
with st.sidebar:
    st.header("Histórico de Chats")
    
    # Botão "New Chat"
    st.button("➕ Novo Chat", on_click=new_chat, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Conversas Recentes")

    # Lista os chats abertos e permite a seleção
    chat_list = list(st.session_state['conversations'].keys())
    
    selected_chat = st.radio(
        "Selecione uma conversa",
        options=chat_list,
        # Define qual chat está selecionado no momento
        index=chat_list.index(st.session_state['current_chat']), 
        key="chat_selector",
        label_visibility="collapsed"
    )

    # Atualiza o estado da sessão quando um chat é selecionado
    if selected_chat != st.session_state['current_chat']:
        st.session_state['current_chat'] = selected_chat
        st.rerun() # Força o rerun para mostrar o histórico correto

# ----------------------------------------------------------------------
# ÁREA PRINCIPAL DO CHAT
# ----------------------------------------------------------------------

st.title("🤖 BeeMo - Assistente Educacional")
st.caption("Eu sou especialista em Cloud Computing, Pyhton e FastAPI, mas você pode me perguntar outras coisas do mundo de computação também. Fui desenvolvido com Python, FastAPI e Gemini API.")

# Obtém o histórico do chat atualmente selecionado na sidebar
current_chat_name = st.session_state['current_chat']
current_messages = st.session_state['conversations'][current_chat_name]

# Exibe a aba de debug em uma área separada (mantido do seu código original)
with st.expander("🔧 Configuração de Debug"):
    st.write(f"**Backend URL:** {FASTAPI_BACKEND_URL}")
    st.write(f"**Endpoint Atual:** {CHAT_ENDPOINT}")
    st.write(f"**Chat Ativo:** {current_chat_name}")
    
    if st.button("Teste de Conexão com o Backend"):
        try:
            test_response = requests.get(f"{FASTAPI_BACKEND_URL}/", timeout=5)
            if test_response.status_code == 200:
                st.success("✅ Conexão com o Backend estabelecida!")
                st.write(test_response.json())
            else:
                st.error(f"❌ Status code: {test_response.status_code}")
        except Exception as e:
            st.error(f"❌ Erro de Conexão: {e}")

# Exibe o histórico de mensagens
for msg in current_messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Captura a entrada do usuário
if prompt := st.chat_input(f"Pergunte em {current_chat_name}..."):
    
    # 1. Adiciona a mensagem do usuário
    current_messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 2. Obtém a resposta do back-end (FastAPI)
    with st.spinner("⏳ Hm...Deixe-me pensar..."):
        full_response = get_chatbot_response(prompt)
    
    # 3. Adiciona a resposta do assistente
    current_messages.append({"role": "assistant", "content": full_response})
    st.chat_message("assistant").write(full_response)
    
    # 4. Atualiza o estado da sessão (salva o histórico do chat ativo)
    st.session_state['conversations'][current_chat_name] = current_messages
    
    # Recarrega a página para atualizar o histórico
    st.rerun()