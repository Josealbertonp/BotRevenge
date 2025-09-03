import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime
import logging
from config import DISCORD_TOKEN, AUDIT_CHANNEL_NAME

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configurações do bot
intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True
intents.message_content = True  # Habilitado para comandos funcionarem

bot = commands.Bot(command_prefix='!', intents=intents)

class AuditLogger:
    """Classe para gerenciar logs de auditoria"""
    
    def __init__(self, bot):
        self.bot = bot
        self.audit_channel_name = AUDIT_CHANNEL_NAME
    
    async def get_audit_channel(self, guild):
        """Busca o canal de auditoria no servidor"""
        for channel in guild.channels:
            if channel.name == self.audit_channel_name:
                return channel
        return None
    
    async def send_audit_log(self, guild, embed):
        """Envia log de auditoria para o canal específico"""
        try:
            audit_channel = await self.get_audit_channel(guild)
            if audit_channel:
                # Verificar se o bot tem permissão para enviar mensagens
                if audit_channel.permissions_for(guild.me).send_messages:
                    await audit_channel.send(embed=embed)
                    logger.info(f"Log de auditoria enviado para {audit_channel.name}")
                else:
                    logger.error(f"Bot não tem permissão para enviar mensagens no canal {audit_channel.name}")
                    # Tentar enviar para o canal geral se disponível
                    await self.send_fallback_log(guild, embed)
            else:
                logger.warning(f"Canal de auditoria '{self.audit_channel_name}' não encontrado")
                # Tentar enviar para o canal geral se disponível
                await self.send_fallback_log(guild, embed)
        except Exception as e:
            logger.error(f"Erro ao enviar log de auditoria: {e}")
    
    async def send_fallback_log(self, guild, embed):
        """Tenta enviar log para um canal alternativo se o canal de auditoria não estiver disponível"""
        try:
            # Procurar por canais onde o bot pode enviar mensagens
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    embed.add_field(name="⚠️ Aviso", value="Canal de auditoria não disponível - enviado para canal alternativo", inline=False)
                    await channel.send(embed=embed)
                    logger.info(f"Log de auditoria enviado para canal alternativo: {channel.name}")
                    return
            logger.error("Nenhum canal disponível para enviar logs de auditoria")
        except Exception as e:
            logger.error(f"Erro ao enviar log de fallback: {e}")
    
    def create_audit_embed(self, action, moderator, target, reason=None, **kwargs):
        """Cria embed para logs de auditoria"""
        embed = discord.Embed(
            title=f"🔍 Log de Auditoria - {action}",
            color=0xff6b6b,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name="👮 Moderador", value=f"{moderator.mention} ({moderator.id})", inline=True)
        embed.add_field(name="🎯 Alvo", value=f"{target.mention} ({target.id})", inline=True)
        
        if reason:
            embed.add_field(name="📝 Motivo", value=reason, inline=False)
        
        # Adicionar campos específicos baseados na ação
        for key, value in kwargs.items():
            if value:
                embed.add_field(name=key, value=value, inline=True)
        
        embed.set_footer(text=f"ID do Servidor: {moderator.guild.id}")
        return embed
    
    def create_voice_embed(self, user, action, channel_name, channel_emoji="💬", moderator=None, guild=None):
        """Cria embed bonito para movimentação de voz como no comando !teste"""
        # Formatar nome do usuário
        user_display = f"@{user.display_name} <{user.name}>"
        
        # Criar embed com barra verde lateral
        embed = discord.Embed(
            title="🔍 Log de Auditoria - Movimentação de Voz",
            description=f"👉🎶 {user_display} {action} {channel_emoji} • {channel_name}",
            color=0x00ff00,  # Verde para barra lateral
            timestamp=datetime.utcnow()
        )
        
        # Adicionar campos
        embed.add_field(name="👤 Usuário", value=f"{user.mention} ({user.id})", inline=True)
        embed.add_field(name="📺 Canal", value=channel_name, inline=True)
        
        if moderator:
            if guild and moderator == guild.me:
                embed.add_field(name="👮 Moderador", value="Sistema/Moderador", inline=True)
                embed.add_field(name="📝 Ação", value="Movido por moderador", inline=True)
            else:
                embed.add_field(name="👮 Moderador", value=f"{moderator.mention} ({moderator.id})", inline=True)
                embed.add_field(name="📝 Ação", value=f"Movido por {moderator.name}", inline=True)
        else:
            embed.add_field(name="📝 Ação", value="Movimentação própria", inline=True)
        
        # Footer com timestamp
        timestamp = datetime.now().strftime("%d/%m/%Y às %H:%M")
        embed.set_footer(text=f"ID do usuário: {user.id} • {timestamp}")
        
        return embed
    
    async def send_voice_embed(self, guild, embed):
        """Envia embed bonito para o canal de auditoria"""
        try:
            audit_channel = await self.get_audit_channel(guild)
            if audit_channel and audit_channel.permissions_for(guild.me).send_messages:
                await audit_channel.send(embed=embed)
                logger.info(f"Embed de voz enviado para {audit_channel.name}")
            else:
                logger.warning(f"Canal de auditoria não disponível para envio")
        except Exception as e:
            logger.error(f"Erro ao enviar embed de voz: {e}")
# Instanciar o logger de auditoria
audit_logger = AuditLogger(bot)

@bot.event
async def on_ready():
    """Evento quando o bot está pronto"""
    logger.info(f'{bot.user} está online!')
    logger.info(f'Bot está em {len(bot.guilds)} servidor(es)')
    logger.info(f'Prefixo do bot: {bot.command_prefix}')
    logger.info(f'Comandos carregados: {[cmd.name for cmd in bot.commands]}')
    
    # Verificar se o canal de auditoria existe em cada servidor
    for guild in bot.guilds:
        audit_channel = await audit_logger.get_audit_channel(guild)
        if audit_channel:
            logger.info(f"Canal de auditoria encontrado em {guild.name}: {audit_channel.name}")
        else:
            logger.warning(f"Canal de auditoria não encontrado em {guild.name}")

@bot.event
async def on_message(message):
    """Evento quando uma mensagem é enviada"""
    # Ignorar mensagens do próprio bot
    if message.author == bot.user:
        return
    
    # Log de debug para comandos
    if message.content.startswith(bot.command_prefix):
        logger.info(f"Comando detectado: {message.content} de {message.author.name}")
    
    # Processar comandos
    await bot.process_commands(message)

# Comentado: on_member_update requer intents privilegiados
# @bot.event
# async def on_member_update(before, after):
#     """Monitora mudanças em membros (timeouts, roles, etc.)"""
#     # Esta funcionalidade requer intents privilegiados
#     pass

@bot.event
async def on_member_ban(guild, user):
    """Monitora quando um usuário é banido"""
    try:
        # Tentar obter informações do ban
        try:
            ban_entry = await guild.fetch_ban(user)
            reason = ban_entry.reason or "Motivo não especificado"
        except:
            reason = "Motivo não disponível"
        
        embed = audit_logger.create_audit_embed(
            action="Usuário Banido",
            moderator=guild.me,  # O bot não pode saber quem baniu
            target=user,
            reason=reason
        )
        
        await audit_logger.send_audit_log(guild, embed)
        logger.info(f"Ban detectado para {user.name}")
    
    except Exception as e:
        logger.error(f"Erro ao processar ban: {e}")

@bot.event
async def on_member_unban(guild, user):
    """Monitora quando um usuário é desbanido"""
    try:
        embed = audit_logger.create_audit_embed(
            action="Usuário Desbanido",
            moderator=guild.me,  # O bot não pode saber quem desbaniu
            target=user,
            reason="Desban detectado"
        )
        
        await audit_logger.send_audit_log(guild, embed)
        logger.info(f"Desban detectado para {user.name}")
    
    except Exception as e:
        logger.error(f"Erro ao processar desban: {e}")

@bot.event
async def on_voice_state_update(member, before, after):
    """Monitora movimentação de usuários entre canais de voz"""
    try:
        # Verificar se o usuário mudou de canal
        if before.channel != after.channel:
            # Tentar detectar quem moveu o usuário usando audit log
            moderator = None
            try:
                # Buscar no audit log quem moveu especificamente este usuário
                current_time = datetime.utcnow().timestamp()
                moderator = None
                
                logger.info(f"🔍 Cruzando dados: {member.name} (ID: {member.id}) com audit log...")
                logger.info(f"⏰ Timestamp atual: {datetime.utcnow().strftime('%H:%M:%S')}")
                
                # Buscar a entrada mais recente de MEMBER_MOVE
                logger.info(f"🔍 Buscando entrada mais recente de MEMBER_MOVE...")
                
                # Pegar apenas a entrada mais recente
                async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_move):
                    if entry.user:
                        moderator = entry.user
                        logger.info(f"📋 ENTRADA MAIS RECENTE:")
                        logger.info(f"   👤 Executor: {entry.user.name} (ID: {entry.user.id})")
                        logger.info(f"   🎯 Target: {entry.target.name if entry.target else 'None'} (ID: {entry.target.id if entry.target else 'None'})")
                        logger.info(f"   ⏰ Timestamp: {entry.created_at.strftime('%H:%M:%S')}")
                        logger.info(f"   📺 Before: {entry.before.channel.name if entry.before and entry.before.channel else 'None'}")
                        logger.info(f"   📺 After: {entry.after.channel.name if entry.after and entry.after.channel else 'None'}")
                        logger.info(f"🎯 Usando entrada mais recente: {moderator.name}")
                        break
                
                if moderator:
                    logger.info(f"🎯 Moderador encontrado: {moderator.name}")
                else:
                    logger.warning(f"❌ Nenhum moderador encontrado para {member.name} (ID: {member.id})")
                            
            except Exception as e:
                logger.warning(f"❌ Não foi possível acessar audit log: {e}")
                moderator = None
            
            # Usuário entrou em um canal
            if not before.channel and after.channel:
                if moderator:
                    embed = audit_logger.create_voice_embed(
                        user=member,
                        action="foi movido para o canal de voz",
                        channel_name=after.channel.name,
                        channel_emoji="💬",
                        moderator=moderator,
                        guild=member.guild
                    )
                else:
                    embed = audit_logger.create_voice_embed(
                        user=member,
                        action="entrou no canal de voz",
                        channel_name=after.channel.name,
                        channel_emoji="💬",
                        guild=member.guild
                    )
                await audit_logger.send_voice_embed(member.guild, embed)
                logger.info(f"Usuário {member.name} entrou no canal {after.channel.name}")
            
            # Usuário saiu de um canal
            elif before.channel and not after.channel:
                if moderator:
                    embed = audit_logger.create_voice_embed(
                        user=member,
                        action="foi removido do canal de voz",
                        channel_name=before.channel.name,
                        channel_emoji="💬",
                        moderator=moderator,
                        guild=member.guild
                    )
                else:
                    embed = audit_logger.create_voice_embed(
                        user=member,
                        action="saiu do canal de voz",
                        channel_name=before.channel.name,
                        channel_emoji="💬",
                        guild=member.guild
                    )
                await audit_logger.send_voice_embed(member.guild, embed)
                logger.info(f"Usuário {member.name} saiu do canal {before.channel.name}")
            
            # Usuário mudou de canal
            elif before.channel and after.channel:
                # Sempre mostrar duas mensagens, mas com o moderador na ação
                embed1 = audit_logger.create_voice_embed(
                    user=member,
                    action="saiu do canal de voz",
                    channel_name=before.channel.name,
                    channel_emoji="💬",
                    moderator=moderator,
                    guild=member.guild
                )
                await audit_logger.send_voice_embed(member.guild, embed1)
                
                embed2 = audit_logger.create_voice_embed(
                    user=member,
                    action="entrou no canal de voz",
                    channel_name=after.channel.name,
                    channel_emoji="💬",
                    moderator=moderator,
                    guild=member.guild
                )
                await audit_logger.send_voice_embed(member.guild, embed2)
                logger.info(f"Usuário {member.name} mudou de {before.channel.name} para {after.channel.name}")
    
    except Exception as e:
        logger.error(f"Erro ao processar mudança de canal de voz: {e}")

# Comentado: on_member_remove requer intents privilegiados
# @bot.event
# async def on_member_remove(member):
#     """Monitora quando um membro sai do servidor"""
#     # Esta funcionalidade requer intents privilegiados
#     pass

# Comando para testar o bot
@bot.command(name='teste')
async def test_command(ctx):
    """Comando para testar se o bot está funcionando"""
    try:
        logger.info(f"Comando !teste executado por {ctx.author.name}")
        
        # Criar embed bonito como no print
        embed = discord.Embed(
            title="🤖 Bot de Auditoria",
            description="Bot funcionando corretamente!",
            color=0x00ff00,  # Verde para barra lateral
            timestamp=datetime.utcnow()
        )
        
        # Adicionar campos
        embed.add_field(name="Status", value="✅ Online", inline=True)
        embed.add_field(name="Canal de Auditoria", value=audit_logger.audit_channel_name, inline=True)
        embed.add_field(name="Servidor", value=ctx.guild.name, inline=True)
        embed.add_field(name="Usuário", value=ctx.author.mention, inline=True)
        
        await ctx.send(embed=embed)
        logger.info("Resposta do comando !teste enviada com sucesso")
        
    except Exception as e:
        logger.error(f"Erro no comando !teste: {e}")
        try:
            await ctx.send(f"❌ Erro no comando: {e}")
        except:
            logger.error("Não foi possível enviar mensagem de erro")

# Comando simples para debug
@bot.command(name='ping')
async def ping_command(ctx):
    """Comando simples para testar conectividade"""
    try:
        await ctx.send("🏓 Pong!")
        logger.info(f"Comando !ping executado por {ctx.author.name}")
    except Exception as e:
        logger.error(f"Erro no comando !ping: {e}")

# Comando para debug
@bot.command(name='debug')
async def debug_command(ctx):
    """Comando para debug do bot"""
    try:
        info = f"""
**Debug do Bot:**
- Bot: {bot.user}
- Servidor: {ctx.guild.name}
- Canal: {ctx.channel.name}
- Usuário: {ctx.author.name}
- Prefixo: {bot.command_prefix}
- Comandos: {len(bot.commands)}
- Intents: {bot.intents}
        """
        await ctx.send(info)
        logger.info(f"Comando !debug executado por {ctx.author.name}")
    except Exception as e:
        logger.error(f"Erro no comando !debug: {e}")

# Comando para testar audit log
@bot.command(name='audit')
async def audit_command(ctx):
    """Comando para testar audit log"""
    try:
        embed = discord.Embed(
            title="📋 Teste de Audit Log",
            description="Verificando se o bot tem acesso ao audit log...",
            color=0x0099ff
        )
        
        # Testar acesso ao audit log
        try:
            # Buscar movimentações recentes
            recent_moves = []
            async for entry in ctx.guild.audit_logs(limit=10, action=discord.AuditLogAction.member_move):
                # Verificar se entry.user e entry.target existem
                if entry.user and entry.target:
                    user_name = entry.user.name if entry.user else "Desconhecido"
                    target_name = entry.target.name if entry.target else "Desconhecido"
                    before_channel = entry.before.channel.name if entry.before and entry.before.channel else "Nenhum"
                    after_channel = entry.after.channel.name if entry.after and entry.after.channel else "Nenhum"
                    timestamp = entry.created_at.strftime("%H:%M:%S")
                    recent_moves.append(f"**{timestamp}** - **{user_name}** moveu **{target_name}** de {before_channel} para {after_channel}")
            
            if recent_moves:
                embed.add_field(name="✅ Audit Log Funcionando", value="O bot tem acesso ao audit log!", inline=False)
                embed.add_field(name="Movimentações Recentes (com timestamp)", value="\n".join(recent_moves[:5]), inline=False)
            else:
                embed.add_field(name="✅ Audit Log Funcionando", value="O bot tem acesso ao audit log, mas não há movimentações recentes.", inline=False)
                
        except Exception as e:
            embed.add_field(name="❌ Audit Log Não Funciona", value=f"Erro: {e}", inline=False)
            embed.add_field(name="Solução", value="O bot precisa da permissão 'View Audit Log'. Siga o guia de reinstalação.", inline=False)
        
        await ctx.send(embed=embed)
        logger.info(f"Comando !audit executado por {ctx.author.name}")
    except Exception as e:
        logger.error(f"Erro no comando !audit: {e}")
        await ctx.send(f"❌ Erro geral: {e}")

@bot.command(name='testmove')
async def test_move_detection(ctx):
    """Testa a detecção de movimentação em tempo real"""
    embed = discord.Embed(
        title="🧪 Teste de Detecção de Movimentação",
        description="Agora mova um usuário de canal para testar a detecção!",
        color=0x00ff00
    )
    embed.add_field(
        name="📋 O que fazer:",
        value="1. Mova um usuário de canal de voz\n2. Verifique os logs no terminal\n3. Veja se aparece o nome do moderador",
        inline=False
    )
    embed.add_field(
        name="⏰ Tempo limite:",
        value="15 segundos para detectar o moderador",
        inline=False
    )
    await ctx.send(embed=embed)

# Comando para verificar configurações
@bot.command(name='config')
async def config_command(ctx):
    """Mostra as configurações atuais do bot"""
    audit_channel = await audit_logger.get_audit_channel(ctx.guild)
    
    embed = discord.Embed(
        title="⚙️ Configurações do Bot",
        color=0x0099ff
    )
    embed.add_field(name="Canal de Auditoria", value=audit_channel.mention if audit_channel else "❌ Não encontrado", inline=True)
    embed.add_field(name="Nome do Canal", value=audit_logger.audit_channel_name, inline=True)
    embed.add_field(name="Servidor", value=ctx.guild.name, inline=True)
    
    # Verificar permissões
    if audit_channel:
        perms = audit_channel.permissions_for(ctx.guild.me)
        embed.add_field(name="Permissões no Canal", value="✅ Enviar Mensagens" if perms.send_messages else "❌ Enviar Mensagens", inline=True)
    
    await ctx.send(embed=embed)

# Comando para verificar permissões
@bot.command(name='perms')
async def perms_command(ctx):
    """Verifica as permissões do bot no servidor"""
    embed = discord.Embed(
        title="🔐 Permissões do Bot",
        color=0xff6b6b
    )
    
    # Verificar permissões gerais do servidor
    general_perms = ctx.guild.me.guild_permissions
    embed.add_field(name="Permissões Gerais", value="", inline=False)
    embed.add_field(name="Ver Canais", value="✅" if general_perms.view_channel else "❌", inline=True)
    embed.add_field(name="Enviar Mensagens", value="✅" if general_perms.send_messages else "❌", inline=True)
    embed.add_field(name="Usar Comandos", value="✅" if general_perms.use_slash_commands else "❌", inline=True)
    
    # Verificar canal de auditoria
    audit_channel = await audit_logger.get_audit_channel(ctx.guild)
    if audit_channel:
        channel_perms = audit_channel.permissions_for(ctx.guild.me)
        embed.add_field(name="Permissões no Canal de Auditoria", value="", inline=False)
        embed.add_field(name="Ver Canal", value="✅" if channel_perms.view_channel else "❌", inline=True)
        embed.add_field(name="Enviar Mensagens", value="✅" if channel_perms.send_messages else "❌", inline=True)
        embed.add_field(name="Enviar Embeds", value="✅" if channel_perms.embed_links else "❌", inline=True)
    else:
        embed.add_field(name="Canal de Auditoria", value="❌ Não encontrado", inline=False)
    
    await ctx.send(embed=embed)

# Comando para mostrar permissões necessárias
@bot.command(name='permissoes')
async def permissoes_command(ctx):
    """Mostra quais permissões o bot precisa ter"""
    embed = discord.Embed(
        title="📋 Permissões Necessárias para o Bot",
        description="Para o bot funcionar corretamente, ele precisa das seguintes permissões:",
        color=0x00ff00
    )
    
    embed.add_field(
        name="🔧 Permissões Básicas (Obrigatórias)",
        value="""
        ✅ **Ver Canais** - Para acessar canais
        ✅ **Enviar Mensagens** - Para enviar logs de auditoria
        ✅ **Usar Comandos de Slash** - Para comandos funcionarem
        ✅ **Ver Histórico de Mensagens** - Para ler mensagens
        ✅ **Conectar** - Para monitorar canais de voz
        """,
        inline=False
    )
    
    embed.add_field(
        name="📝 Permissões no Canal de Auditoria",
        value="""
        ✅ **Ver Canal** - Para acessar o canal
        ✅ **Enviar Mensagens** - Para enviar logs
        ✅ **Enviar Embeds** - Para mensagens formatadas
        ✅ **Anexar Arquivos** - Para logs detalhados
        """,
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Como Configurar",
        value="""
        1. Vá em **Configurações do Servidor**
        2. **Integrações** → **Bots**
        3. Encontre seu bot e clique em **Configurar**
        4. Ative as permissões listadas acima
        5. Salve as configurações
        """,
        inline=False
    )
    
    embed.add_field(
        name="🔗 Link Direto",
        value="[Portal do Desenvolvedor Discord](https://discord.com/developers/applications/)",
        inline=False
    )
    
    await ctx.send(embed=embed)

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        logger.error("Token do Discord não encontrado!")
        exit(1)
    
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Erro ao iniciar o bot: {e}")
