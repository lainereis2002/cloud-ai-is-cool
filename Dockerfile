# ----------------------------------------------------
# STAGE 1: Build - Instala as dependências (requirements.txt)
# ----------------------------------------------------
# Usa uma imagem Python mais completa como base para o build
FROM python:3.11-slim as builder

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de dependências para o contêiner
COPY requirements.txt .

# Instala todas as dependências do Python
# O flag --no-cache-dir é para evitar arquivos de cache desnecessários na imagem final
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------
# STAGE 2: Final/Runtime - Cria a imagem de produção
# ----------------------------------------------------
# Usa uma imagem Python mínima para o ambiente de execução
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia as dependências instaladas do stage 'builder' para o ambiente final
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copia o código da aplicação (main.py, etc.)
COPY . .

# Expõe a porta que o Uvicorn usará. O padrão para serviços web é 80 ou 8000.
EXPOSE 80

# Comando para rodar a aplicação usando o Uvicorn.
# É importante usar 0.0.0.0 e a porta 80 para que funcione corretamente no ambiente de deploy.
# Comando para rodar a aplicação usando o Uvicorn via módulo Python
CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]