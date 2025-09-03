import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do bot
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')  # Adicione seu token aqui
AUDIT_CHANNEL_NAME = os.getenv('AUDIT_CHANNEL_NAME', '🔐╺╸auditoria')

# Configurações de logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'bot.log')

# Configurações de intents
INTENTS = {
    'guilds': True,
    'voice_states': True
}
