#!/usr/bin/env python
"""
Script de teste para verificar se a API FastAPI está funcionando corretamente.
"""

import requests
import json
import time

BACKEND_URL = "http://127.0.0.1:8000"

def test_health_check():
    """Testa o endpoint de health check."""
    print("\n" + "="*60)
    print("🏥 Testando Health Check...")
    print("="*60)
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_debug_config():
    """Testa o endpoint de debug config."""
    print("\n" + "="*60)
    print("🔧 Testando Debug Config...")
    print("="*60)
    try:
        response = requests.get(f"{BACKEND_URL}/debug/config", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_chat():
    """Testa o endpoint de chat."""
    print("\n" + "="*60)
    print("💬 Testando Endpoint de Chat...")
    print("="*60)
    try:
        payload = {"message": "Olá, como você funciona?"}
        print(f"Enviando: {json.dumps(payload, ensure_ascii=False)}")
        
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload,
            timeout=60,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Resposta: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"Erro: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Erro: Requisição expirou (timeout de 60 segundos)")
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Erro: Não foi possível conectar ao backend em {BACKEND_URL}")
        print("   Verifique se o servidor FastAPI está rodando:")
        print("   uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Erro: {type(e).__name__}: {e}")
        return False

def main():
    print("\n" + "🚀 "*20)
    print("TESTE DE API - ASSISTENTE DE ESTUDOS")
    print("🚀 "*20)
    
    # Teste 1: Health Check
    health_ok = test_health_check()
    time.sleep(1)
    
    # Teste 2: Debug Config
    debug_ok = test_debug_config()
    time.sleep(1)
    
    # Teste 3: Chat
    chat_ok = test_chat()
    
    # Resumo
    print("\n" + "="*60)
    print("📋 RESUMO DOS TESTES")
    print("="*60)
    print(f"✅ Health Check: {'PASSOU' if health_ok else 'FALHOU'}")
    print(f"✅ Debug Config: {'PASSOU' if debug_ok else 'FALHOU'}")
    print(f"✅ Chat: {'PASSOU' if chat_ok else 'FALHOU'}")
    print("="*60)
    
    if health_ok and chat_ok:
        print("\n✨ TODOS OS TESTES PASSARAM! A API está funcionando perfeitamente!")
    else:
        print("\n⚠️  Alguns testes falharam. Verifique os logs acima.")

if __name__ == "__main__":
    main()
