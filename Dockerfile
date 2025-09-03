# Usar Python 3.11 que é estável e compatível
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro (para cache do Docker)
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do bot
COPY . .

# Criar usuário não-root para segurança
RUN useradd --create-home --shell /bin/bash bot && \
    chown -R bot:bot /app
USER bot

# Comando para executar o bot
CMD ["python", "bot.py"]
