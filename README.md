# 🛡️ BotRevenge - Discord Audit Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-green.svg)](https://github.com/Rapptz/discord.py)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Um bot Discord avançado para monitoramento de auditoria em tempo real, com detecção inteligente de movimentações de voz e ações administrativas.

## ✨ Funcionalidades

### 🎯 Monitoramento de Voz
- **Detecção de movimentações** entre canais de voz
- **Identificação do moderador** que moveu o usuário
- **Logs em tempo real** com embeds visuais
- **Cruzamento de dados** com audit log do Discord

### 🔍 Sistema de Auditoria
- **Monitoramento de bans** e unbans
- **Logs detalhados** de todas as ações
- **Embeds visuais** com informações completas
- **Canal dedicado** para auditoria

### 🎨 Interface Visual
- **Embeds coloridos** com barra lateral verde
- **Informações organizadas** em campos
- **Timestamps precisos** em todas as ações
- **Design responsivo** e profissional

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Conta Discord com servidor
- Bot Discord criado no [Discord Developer Portal](https://discord.com/developers/applications)

### 1. Clone o repositório
```bash
git clone https://github.com/Josealbertonp/BotRevenge.git
cd BotRevenge
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure o bot
Crie um arquivo `.env` na raiz do projeto:
```bash
# .env
DISCORD_TOKEN=seu_token_aqui
AUDIT_CHANNEL_NAME=🔐╺╸auditoria
```

**⚠️ IMPORTANTE:** Nunca compartilhe seu token do Discord!

### 4. Execute o bot
```bash
python3 bot.py
```

## ⚙️ Configuração

### Permissões Necessárias
O bot precisa das seguintes permissões:

#### Permissões Básicas
- ✅ **View Channels** - Ver canais
- ✅ **Send Messages** - Enviar mensagens
- ✅ **Embed Links** - Enviar embeds
- ✅ **Read Message History** - Ler histórico

#### Permissões de Auditoria
- ✅ **View Audit Log** - **CRÍTICO!** Para detectar quem moveu usuários
- ✅ **Move Members** - Mover membros (opcional)
- ✅ **Ban Members** - Banir membros (opcional)

### Intents Necessários
Habilite os seguintes intents no Discord Developer Portal:

- ✅ **Server Members Intent** - Para monitorar membros
- ✅ **Message Content Intent** - Para comandos com prefixo
- ✅ **Guilds Intent** - Para acessar servidores
- ✅ **Voice States Intent** - Para monitorar canais de voz

## 📋 Comandos

### Comandos de Teste
- `!teste` - Testa se o bot está funcionando
- `!ping` - Testa conectividade
- `!testmove` - Testa detecção de movimentação

### Comandos de Diagnóstico
- `!debug` - Informações detalhadas do bot
- `!audit` - Testa acesso ao audit log
- `!perms` - Verifica permissões do bot
- `!config` - Mostra configurações atuais

### Comandos de Ajuda
- `!help` - Lista todos os comandos
- `!permissoes` - Lista permissões necessárias

## 🔧 Estrutura do Projeto

```
BotRevenge/
├── 📄 bot.py              # Arquivo principal do bot
├── 📄 config.py           # Configurações
├── 📄 requirements.txt    # Dependências
├── 📄 README.md          # Documentação completa
├── 📄 LICENSE            # Licença MIT
└── 📄 .gitignore         # Arquivos ignorados pelo Git
```

## 🎯 Como Funciona

### Detecção de Movimentação
1. **Evento de voz** é detectado pelo Discord
2. **Audit log** é consultado para encontrar o executor
3. **Cruzamento de dados** identifica quem moveu o usuário
4. **Embed visual** é enviado para o canal de auditoria

### Sistema de Fallback
- Se não conseguir detectar o moderador, usa "Sistema/Moderador"
- Se o audit log não estiver acessível, registra como "Movimentação própria"
- Logs detalhados para debug e troubleshooting

## 🛠️ Desenvolvimento

### Executar o Bot
```bash
python3 bot.py
```

## 📊 Logs e Monitoramento

O bot gera logs detalhados incluindo:
- ✅ Conexão e status do bot
- ✅ Detecção de movimentações
- ✅ Acesso ao audit log
- ✅ Envio de embeds
- ✅ Erros e exceções

## 🔒 Segurança

- **Token protegido** em arquivo de configuração
- **Permissões mínimas** necessárias
- **Logs seguros** sem exposição de dados sensíveis
- **Validação de entrada** em todos os comandos

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🆘 Suporte

### Problemas Comuns

#### Bot não responde aos comandos
- Verifique se o **Message Content Intent** está habilitado
- Confirme se o bot tem permissão para enviar mensagens

#### Não detecta quem moveu usuários
- Verifique se o **View Audit Log** está habilitado
- Confirme se o bot tem a permissão "View Audit Log"

#### Erro de permissões
- Verifique as permissões no Discord Developer Portal
- Reinstale o bot com as permissões corretas

### Links Úteis
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord API Documentation](https://discord.com/developers/docs)

## 🎉 Agradecimentos

- [Discord.py](https://github.com/Rapptz/discord.py) - Biblioteca Python para Discord
- [Discord](https://discord.com/) - Plataforma de comunicação

---

**Desenvolvido com ❤️ para monitoramento de auditoria em Discord**
