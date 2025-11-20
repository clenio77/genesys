"""
Handlers para comandos do bot
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode
from datetime import datetime

from shared.utils.logger import bot_telegram_logger as logger
from handlers.messages import safe_reply_text


async def safe_send_typing(chat):
    """
    Envia indicador de digitação de forma segura, ignorando timeouts
    Não falha o comando se houver problema de conexão
    """
    try:
        await chat.send_action("typing")
    except Exception as e:
        # Ignorar timeouts e outros erros de conexão - não é crítico
        logger.debug(f"Erro ao enviar indicador de digitação (ignorando): {type(e).__name__}")
        pass


async def cmd_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /menu - Menu principal profissional"""
    await safe_send_typing(update.message.chat)
    
    try:
        from services.auth_service import auth_service
        from utils.message_formatter import message_formatter
        from shared.config.database import get_db
        from shared.database.models import User
        
        user_id = update.effective_user.id
        is_auth = auth_service.is_authenticated(user_id)
        
        # Buscar último acesso se autenticado
        ultimo_acesso = None
        if is_auth:
            try:
                db = next(get_db())
                user = db.query(User).filter(User.telegram_id == user_id).first()
                if user and user.ultimo_login:
                    ultimo_acesso = user.ultimo_login.strftime("%d/%m/%Y %H:%M")
                db.close()
            except:
                pass
        
        menu = message_formatter.formatar_menu_principal(is_auth, ultimo_acesso)
        await update.message.reply_text(menu, parse_mode=ParseMode.MARKDOWN)
        
    except Exception as e:
        logger.error(f"Erro no comando /menu: {e}")
        await update.message.reply_text(
            "🎯 **Menu Principal**\n\nUse /help para ver todos os comandos disponíveis.",
            parse_mode=ParseMode.MARKDOWN
        )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help"""
    await safe_send_typing(update.message.chat)
    
    from services.auth_service import auth_service
    
    user_id = update.effective_user.id
    is_auth = auth_service.is_authenticated(user_id)
    
    help_text = f"""
📚 **Comandos Disponíveis:**

🎯 **Navegação:**
/menu - Menu principal interativo
/help - Ver esta ajuda
/start - Reiniciar o bot

📚 **Consultas:**
/processo - Consultar status de processo (API CNJ + base local)
/buscar - Buscar jurisprudência
/magistrado - Buscar perfil de magistrado {'✅' if is_auth else '🔒'}
{'/promotor - Buscar perfil de promotor ✅' if is_auth else '/promotor - Buscar perfil de promotor 🔒'}
{'/comarca - Processos por comarca ✅' if is_auth else '/comarca - Processos por comarca 🔒'}
{'/comparar - Comparar magistrados ou promotores ✅' if is_auth else '/comparar - Comparar magistrados 🔒'}
{'/padroes - Análise de padrões de julgamento ✅' if is_auth else '/padroes - Análise de padrões 🔒'}

📊 **Gestão:**
/prazos - Ver prazos processuais pendentes
/alerta - Configurar alertas
/historico - Histórico de consultas
/estatisticas - Estatísticas gerais do Kermartin

⚙️ **Configurações:**
/perfil - Meu perfil
/config - Configurações
/cache - Estatísticas de cache e memória
/status - Status de autenticação

🔐 **Autenticação:**
{'/logout - Fazer logout ✅' if is_auth else '/login - Fazer login para acessar Kermartin'}
{'/trocar_senha - Trocar senha ✅' if is_auth else '/cadastrar - Cadastrar email e senha'}
{'/recuperar_senha - Recuperar senha usando código' if not is_auth else ''}

💡 **Dica:** Você também pode fazer perguntas em linguagem natural e eu tentarei ajudar!
"""
    await safe_reply_text(update, help_text, use_markdown=True)


async def cmd_buscar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /buscar - Buscar jurisprudência"""
    await safe_send_typing(update.message.chat)
    
    try:
        from services.jurisprudencia_service import jurisprudencia_service
        
        # Armazenar o estado de busca
        context.user_data['aguardando_busca'] = True
        
        await update.message.reply_text(
            "🔍 **Busca de Jurisprudência**\n\n"
            "Envie o tema ou questão jurídica que deseja buscar.\n\n"
            "**Exemplos:**\n"
            "• `indenização por danos morais`\n"
            "• `precedentes sobre CLT`\n"
            "• `jurisprudência trabalhista`\n\n"
            "**Filtros disponíveis:**\n"
            "• `--tribunal TJMG` - Filtrar por tribunal\n"
            "• `--data 2024` - Filtrar por ano\n"
            "• `--assunto criminal` - Filtrar por assunto\n"
            "• `--magistrado Nome` - Filtrar por magistrado\n"
            "• `--limite 10` - Limitar resultados\n\n"
            "**Exemplo com filtros:**\n"
            "`homicídio qualificado --tribunal TJMG --data 2024 --limite 5`\n\n"
            "💡 Eu buscarei em nossa base de decisões com IA!",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error(f"Erro no comando /buscar: {e}")
        await update.message.reply_text(
            "🔍 Busca de jurisprudência. Digite sua consulta jurídica.",
            parse_mode=ParseMode.MARKDOWN
        )


async def cmd_prazos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /prazos - Listar prazos pendentes"""
    # Mostrar indicador de digitação
    await safe_send_typing(update.message.chat)
    
    try:
        from services.prazos_service import prazos_service
        from services.database_service import db_service
        from shared.config.database import get_db
        from shared.database.models import User
        
        user_id = update.effective_user.id
        
        try:
            # Buscar usuário
            db = next(get_db())
            user = db.query(User).filter(User.telegram_id == user_id).first()
            db.close()
            
            if user:
                # Buscar prazos reais do banco
                prazos = db_service.get_user_prazos(user.id)
                
                # Sincronizar com Kermartin se autenticado
                try:
                    from services.auth_service import auth_service
                    if auth_service.is_authenticated(user_id):
                        prazos_kermartin = prazos_service.sincronizar_prazos_kermartin(user.id, user_id)
                        # Adicionar prazos do Kermartin ao resultado
                        # (por enquanto apenas mostrar, pode ser melhorado para salvar no banco)
                        if prazos_kermartin:
                            resposta = prazos_service.formatar_prazos(prazos)
                            resposta += "\n\n" + "─" * 35 + "\n\n"
                            resposta += "📊 **Prazos Sincronizados do Kermartin:**\n\n"
                            for prazo_k in prazos_kermartin[:5]:
                                dias_restantes = (prazo_k['data_vencimento'].date() - datetime.now().date()).days
                                emoji = "🔴" if dias_restantes <= 1 else "🟡" if dias_restantes <= 3 else "🟢"
                                resposta += f"{emoji} **{prazo_k['tipo']}**\n"
                                resposta += f"📄 Processo: `{prazo_k['processo']}`\n"
                                resposta += f"📅 Vence em: {prazo_k['data_vencimento'].strftime('%d/%m/%Y')}\n"
                                resposta += f"⏰ {dias_restantes} dias restantes\n\n"
                            resposta += "💡 Prazos calculados automaticamente das movimentações do Kermartin"
                        else:
                            resposta = prazos_service.formatar_prazos(prazos)
                    else:
                        resposta = prazos_service.formatar_prazos(prazos)
                except Exception as e:
                    logger.warning(f"Erro ao sincronizar prazos com Kermartin: {e}")
                    resposta = prazos_service.formatar_prazos(prazos)
            else:
                # Usar prazos de exemplo
                resposta = prazos_service.criar_prazo_exemplo(user_id)
            
            await update.message.reply_text(resposta, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as db_error:
            logger.warning(f"Banco de dados não disponível: {db_error}")
            # Mostrar prazos de exemplo
            resposta = prazos_service.criar_prazo_exemplo(user_id)
            await update.message.reply_text(resposta, parse_mode=ParseMode.MARKDOWN)
            
    except Exception as e:
        logger.error(f"Erro ao buscar prazos: {e}")
        await update.message.reply_text(
            "📅 **Seus Prazos Processuais**\n\n"
            "⚠️ Não foi possível acessar seus prazos agora.\n"
            "Use /alerta para configurar notificações.",
            parse_mode=ParseMode.MARKDOWN
        )


async def cmd_alerta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /alerta - Configurar alertas"""
    await safe_send_typing(update.message.chat)
    
    try:
        # Buscar preferências atuais do usuário
        from services.alertas_service import alertas_service
        from services.database_service import db_service
        
        user = db_service.get_or_create_user(
            update.effective_user.id,
            update.effective_user.username or "User",
            update.effective_user.full_name or "User"
        )
        
        prefs = None
        if user:
            prefs = alertas_service.get_user_alert_preferences(user.id)
        
        # Montar mensagem com status atual
        if prefs:
            canal_emoji = "📧" if prefs["canal"] == "email" else "📱"
            canal_nome = prefs["canal"].upper()
            intervalo = prefs["intervalo_dias"]
            status = "✅ Ativo" if prefs["ativo"] else "❌ Desativado"
            
            status_text = f"""⚙️ **Configuração de Alertas de Prazos**

**Status Atual:**
{canal_emoji} Canal: {canal_nome}
⏰ Intervalo: {intervalo} dias antes
🔔 Status: {status}

**Escolha como deseja receber alertas:**"""
        else:
            status_text = """⚙️ **Configuração de Alertas de Prazos**

Escolha como deseja receber seus alertas de prazos processuais:"""
        
    except Exception as e:
        logger.error(f"Erro ao buscar preferências: {e}")
        status_text = """⚙️ **Configuração de Alertas de Prazos**

Escolha como deseja receber seus alertas de prazos processuais:"""
    
    keyboard = [
        [
            InlineKeyboardButton("📧 Via Email", callback_data="alerta_email"),
            InlineKeyboardButton("📱 Via Telegram", callback_data="alerta_telegram")
        ],
        [
            InlineKeyboardButton("⏰ 7 dias antes", callback_data="intervalo_7"),
            InlineKeyboardButton("⏰ 3 dias antes", callback_data="intervalo_3"),
            InlineKeyboardButton("⏰ 1 dia antes", callback_data="intervalo_1")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        status_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )


async def cmd_processo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /processo - Consultar processo via API CNJ (e Kermartin se autenticado)"""
    await safe_send_typing(update.message.chat)
    
    # Verificar autenticação para acesso ao Kermartin (mas permite API CNJ sem login)
    from services.auth_service import auth_service
    
    user_id = update.effective_user.id
    is_auth = auth_service.is_authenticated(user_id)
    
    # Marcar que está aguardando número do processo
    context.user_data['aguardando_processo'] = True
    context.user_data['usuario_autenticado'] = is_auth
    
    auth_note = ""
    if is_auth:
        auth_note = "\n✅ **Você está autenticado!** Também buscarei na base Kermartin.\n"
    else:
        auth_note = (
            "\n⚠️ **Acesso limitado:** Sem login, apenas API CNJ disponível.\n"
            "💡 Use `/login` para acessar também dados do Kermartin.\n"
        )
    
    await update.message.reply_text(
        "⚖️ **Consulta de Processo**\n\n"
        "🔍 Envie o número do processo no formato CNJ:\n\n"
        "**Formato:** NNNNNNN-DD.AAAA.J.TR.OOOO\n\n"
        "**Exemplo:**\n"
        "`0001234-56.2024.8.26.0100`\n\n"
        "💡 Eu consultarei na API Pública do CNJ e te mostrarei:\n"
        "• Status do processo\n"
        "• Última movimentação\n"
        "• Dados principais\n"
        + auth_note +
        "\n📝 Envie o número agora:",
        parse_mode=ParseMode.MARKDOWN
    )


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /status - Mostra status de autenticação"""
    await safe_send_typing(update.message.chat)
    
    try:
        from services.auth_service import auth_service
        from utils.message_formatter import message_formatter
        from shared.config.database import get_db
        from shared.database.models import User
        
        user_id = update.effective_user.id
        is_auth = auth_service.is_authenticated(user_id)
        
        ultimo_login = None
        sessao_expira = None
        
        if is_auth:
            try:
                db = next(get_db())
                user = db.query(User).filter(User.telegram_id == user_id).first()
                if user:
                    if user.ultimo_login:
                        ultimo_login = user.ultimo_login.strftime("%d/%m/%Y %H:%M")
                    # Calcular expiração (24h após último login)
                    if user.ultimo_login:
                        from datetime import timedelta
                        expira = user.ultimo_login + timedelta(hours=24)
                        sessao_expira = expira.strftime("%d/%m/%Y %H:%M")
                db.close()
            except Exception as e:
                logger.warning(f"Erro ao buscar dados do usuário: {e}")
        
        status = message_formatter.formatar_status_auth(is_auth, ultimo_login, sessao_expira)
        await update.message.reply_text(status, parse_mode=ParseMode.MARKDOWN)
        
    except Exception as e:
        logger.error(f"Erro no comando /status: {e}")
        await update.message.reply_text(
            "⚠️ Erro ao verificar status. Tente novamente.",
            parse_mode=ParseMode.MARKDOWN
        )


async def cmd_magistrado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /magistrado - Buscar perfil de magistrado"""
    await safe_send_typing(update.message.chat)
    
    # Verificar autenticação para acessar Kermartin (com verificação de timeout)
    from services.auth_service import auth_service
    
    user_id = update.effective_user.id
    is_auth = auth_service.is_authenticated(user_id, check_timeout=True)
    
    if not is_auth:
        # Verificar se foi timeout ou apenas não autenticado
        if auth_service.is_authenticated(user_id, check_timeout=False):
            # Sessão expirada
            await update.message.reply_text(
                "⏰ **Sessão Expirada**\n\n"
                "Sua sessão expirou após 24 horas de inatividade.\n\n"
                "💡 Faça login novamente com `/login` para continuar usando o Kermartin.",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            # Não autenticado
            await update.message.reply_text(
                auth_service.require_auth_message(),
                parse_mode=ParseMode.MARKDOWN
            )
        return
    
    # Marcar que está aguardando nome do magistrado
    context.user_data['aguardando_magistrado'] = True
    
    await update.message.reply_text(
        "👨‍⚖️ **Consulta de Magistrado**\n\n"
        "🔍 Envie o nome do magistrado que deseja buscar:\n\n"
        "**Exemplos:**\n"
        "• Dimas Borges de Paula\n"
        "• Rui Magalhães\n"
        "• Paulo Caixeta\n\n"
        "💡 Vou buscar na base de conhecimento Kermartin:\n"
        "• Perfil completo\n"
        "• Estatísticas de julgados\n"
        "• Especialização\n"
        "• Histórico de decisões\n\n"
        "📝 Envie o nome agora:",
        parse_mode=ParseMode.MARKDOWN
    )


async def cmd_promotor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /promotor - Buscar perfil de promotor"""
    await safe_send_typing(update.message.chat)
    
    # Verificar autenticação para acessar Kermartin (com verificação de timeout)
    from services.auth_service import auth_service
    
    user_id = update.effective_user.id
    is_auth = auth_service.is_authenticated(user_id, check_timeout=True)
    
    if not is_auth:
        # Verificar se foi timeout ou apenas não autenticado
        if auth_service.is_authenticated(user_id, check_timeout=False):
            await update.message.reply_text(
                "⏰ **Sessão Expirada**\n\n"
                "Sua sessão expirou após 24 horas de inatividade.\n\n"
                "💡 Faça login novamente com `/login` para continuar usando o Kermartin.",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                auth_service.require_auth_message(),
                parse_mode=ParseMode.MARKDOWN
            )
        return
    
    # Marcar que está aguardando nome do promotor
    context.user_data['aguardando_promotor'] = True
    
    await update.message.reply_text(
        "👤 **Consulta de Promotor**\n\n"
        "🔍 Envie o nome do promotor que deseja buscar:\n\n"
        "**Exemplos:**\n"
        "• Arthur Machado Ribeiro\n"
        "• Bruna Gonçalves Ferreira\n"
        "• Danielle Louise Rutkowski\n\n"
        "💡 Vou buscar na base de conhecimento Kermartin:\n"
        "• Perfil completo\n"
        "• Histórico de atuações\n"
        "• Casos relacionados\n"
        "• Estatísticas\n\n"
        "📝 Envie o nome agora:",
        parse_mode=ParseMode.MARKDOWN
    )


async def cmd_comarca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /comarca - Buscar processos por comarca"""
    await safe_send_typing(update.message.chat)
    
    # Verificar autenticação para acessar Kermartin (com verificação de timeout)
    from services.auth_service import auth_service
    
    user_id = update.effective_user.id
    is_auth = auth_service.is_authenticated(user_id, check_timeout=True)
    
    if not is_auth:
        # Verificar se foi timeout ou apenas não autenticado
        if auth_service.is_authenticated(user_id, check_timeout=False):
            await update.message.reply_text(
                "⏰ **Sessão Expirada**\n\n"
                "Sua sessão expirou após 24 horas de inatividade.\n\n"
                "💡 Faça login novamente com `/login` para continuar usando o Kermartin.",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                auth_service.require_auth_message(),
                parse_mode=ParseMode.MARKDOWN
            )
        return
    
    # Marcar que está aguardando nome da comarca
    context.user_data['aguardando_comarca'] = True
    
    await update.message.reply_text(
        "🏛️ **Consulta de Processos por Comarca**\n\n"
        "🔍 Envie o nome da comarca que deseja buscar:\n\n"
        "**Exemplos:**\n"
        "• `Uberlândia`\n"
        "• `Uberaba --tipo criminal`\n"
        "• `Araguari --status julgado --limite 10`\n"
        "• `Patos de Minas --tipo trabalhista`\n\n"
        "**Filtros disponíveis:**\n"
        "• `--tipo tipo_processo` - Filtrar por tipo (criminal, trabalhista, etc)\n"
        "• `--status status` - Filtrar por status (julgado, em andamento, etc)\n"
        "• `--limite numero` - Limitar número de resultados (padrão: 50)\n\n"
        "💡 Vou buscar na base de dados Kermartin:\n"
        "• Processos da comarca\n"
        "• Informações detalhadas\n"
        "• Status dos processos\n"
        "• Estatísticas\n\n"
        "📝 Envie o nome da comarca agora:",
        parse_mode=ParseMode.MARKDOWN
    )


async def cmd_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /config - Configurações"""
    await safe_send_typing(update.message.chat)
    
    config_text = """
⚙️ **Configurações**

🔔 Notificações: Ativadas
📧 Email: cadastrado
📱 Telegram: Ativo
🌐 Idioma: Português (BR)

Use os botões abaixo para alterar:
"""
    
    keyboard = [
        [
            InlineKeyboardButton("🔔 Notificações", callback_data="config_notif"),
            InlineKeyboardButton("📧 Email", callback_data="config_email")
        ],
        [
            InlineKeyboardButton("📱 Telegram", callback_data="config_telegram"),
            InlineKeyboardButton("🌐 Idioma", callback_data="config_idioma")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        config_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )


async def cmd_estatisticas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /estatisticas - Estatísticas gerais do Kermartin"""
    await safe_send_typing(update.message.chat)
    
    try:
        from services.kermartin_service import kermartin_service
        from services.database_service import db_service
        from utils.message_formatter import message_formatter
        
        user_id = update.effective_user.id
        
        # Buscar estatísticas do Kermartin
        stats = kermartin_service.get_estatisticas_gerais()
        
        # Buscar estatísticas de uso do bot
        historico = db_service.get_historico_consultas(user_id, limit=1000)
        total_consultas = len(historico)
        
        tipos_consulta = {}
        for item in historico:
            tipo = item.get('tipo', 'geral')
            tipos_consulta[tipo] = tipos_consulta.get(tipo, 0) + 1
        
        stats_text = f"""📊 **Estatísticas Gerais - Kermartin**

{'═' * 35}

📚 **Base de Conhecimento:**
• Magistrados: {stats['magistrados']}
• Promotores: {stats['promotores']}
• Processos coletados: {stats['processos']}
• Comarcas: {len(stats['comarcas'])}
• Tribunais: {len(stats['tribunais'])}"""
        
        if stats['comarcas']:
            stats_text += f"\n\n📍 **Comarcas Disponíveis:**\n"
            for comarca in sorted(stats['comarcas'])[:10]:
                stats_text += f"   • {comarca}\n"
            if len(stats['comarcas']) > 10:
                stats_text += f"   ... e mais {len(stats['comarcas']) - 10} comarca(s)\n"
        
        if stats['tipos_processo']:
            stats_text += f"\n📋 **Tipos de Processo:**\n"
            tipos_ordenados = sorted(stats['tipos_processo'].items(), key=lambda x: x[1], reverse=True)[:5]
            for tipo, count in tipos_ordenados:
                stats_text += f"   • {tipo}: {count}\n"
        
        if stats['status_processos']:
            stats_text += f"\n⚖️ **Status dos Processos:**\n"
            status_ordenados = sorted(stats['status_processos'].items(), key=lambda x: x[1], reverse=True)[:5]
            for status, count in status_ordenados:
                stats_text += f"   • {status}: {count}\n"
        
        stats_text += f"\n{'─' * 35}\n\n"
        stats_text += f"🤖 **Seu Uso do Bot:**\n"
        stats_text += f"• Total de consultas: {total_consultas}\n"
        
        if tipos_consulta:
            stats_text += f"• Por tipo:\n"
            for tipo, count in sorted(tipos_consulta.items(), key=lambda x: x[1], reverse=True):
                icon = {'processo': '⚖️', 'magistrado': '👨‍⚖️', 'promotor': '👤', 'buscar': '🔍'}.get(tipo, '📝')
                stats_text += f"   {icon} {tipo}: {count}\n"
        
        stats_text += "\n" + "─" * 35 + "\n"
        stats_text += message_formatter.footer()
        
        await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {e}")
        await update.message.reply_text(
            "⚠️ Erro ao obter estatísticas. Tente novamente.",
            parse_mode=ParseMode.MARKDOWN
        )


async def cmd_cache_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /cache - Mostra estatísticas de cache e memória"""
    await safe_send_typing(update.message.chat)
    
    try:
        from services.cache_service import cache_service
        
        stats = cache_service.get_stats()
        memory_info = cache_service.get_memory_info()
        
        stats_text = f"""📊 **Estatísticas de Cache**

**Cache:**
• Entradas: {stats['entries']}
• Hits: {stats['hits']}
• Misses: {stats['misses']}
• Taxa de acerto: {stats['hit_rate_percent']}%
• Evicções: {stats['evictions']}

**Memória:**
• Cache usado: {stats['memory_mb']} MB / {stats['max_memory_mb']} MB
• Uso: {stats['memory_usage_percent']}%"""
        
        if memory_info.get('psutil_available'):
            stats_text += f"""

**Memória do Processo:**
• RSS: {memory_info['rss_mb']} MB
• VMS: {memory_info['vms_mb']} MB"""
        else:
            stats_text += f"\n\n💡 {memory_info.get('note', '')}"
        
        await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas de cache: {e}")
        await update.message.reply_text(
            "⚠️ Erro ao obter estatísticas de cache.",
            parse_mode=ParseMode.MARKDOWN
        )


async def cmd_historico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /historico - Histórico de consultas"""
    await safe_send_typing(update.message.chat)
    
    from services.database_service import db_service
    from utils.message_formatter import message_formatter
    
    user_id = update.effective_user.id
    
    # Verificar argumentos
    args = context.args or []
    tipo = None
    limpar = False
    
    if args:
        if args[0].lower() == 'limpar':
            limpar = True
            tipo = args[1].lower() if len(args) > 1 else None
        else:
            tipo = args[0].lower()
    
    try:
        if limpar:
            # Limpar histórico
            sucesso, mensagem = db_service.limpar_historico(user_id, tipo)
            await update.message.reply_text(mensagem, parse_mode=ParseMode.MARKDOWN)
            return
        
        # Buscar histórico
        historico = db_service.get_historico_consultas(user_id, tipo, limit=10)
        
        if not historico:
            tipo_texto = f" de '{tipo}'" if tipo else ""
            await update.message.reply_text(
                f"📋 **Histórico{tipo_texto}**\n\n"
                "Você ainda não tem consultas registradas.\n\n"
                "💡 Faça consultas usando os comandos:\n"
                "• `/processo` - Consultar processo\n"
                "• `/magistrado` - Buscar magistrado\n"
                "• `/promotor` - Buscar promotor\n"
                "• `/buscar` - Buscar jurisprudência",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Formatar histórico
        tipo_texto = f" - {tipo.upper()}" if tipo else ""
        historico_text = f"📋 **Histórico de Consultas{tipo_texto}**\n\n"
        historico_text += "─" * 35 + "\n\n"
        
        # Ícones por tipo
        tipo_icons = {
            'processo': '⚖️',
            'magistrado': '👨‍⚖️',
            'promotor': '👤',
            'buscar': '🔍',
            'geral': '💬'
        }
        
        for i, item in enumerate(historico, 1):
            icon = tipo_icons.get(item['tipo'], '📝')
            data_str = item['data'].strftime("%d/%m/%Y %H:%M") if item['data'] else "N/A"
            
            historico_text += f"**{i}.** {icon} **{item['tipo'].upper()}**\n"
            historico_text += f"   📅 {data_str}\n"
            historico_text += f"   🔍 Consulta: `{item['consulta']}`\n"
            
            if item.get('resposta'):
                resposta_curta = item['resposta'][:80] + '...' if len(item['resposta']) > 80 else item['resposta']
                historico_text += f"   💬 Resposta: {resposta_curta}\n"
            
            historico_text += "\n"
        
        historico_text += "─" * 35 + "\n\n"
        historico_text += "💡 **Comandos disponíveis:**\n"
        historico_text += "• `/historico` - Ver todas as consultas\n"
        historico_text += "• `/historico processo` - Apenas processos\n"
        historico_text += "• `/historico magistrado` - Apenas magistrados\n"
        historico_text += "• `/historico promotor` - Apenas promotores\n"
        historico_text += "• `/historico buscar` - Apenas buscas\n"
        historico_text += "• `/historico limpar` - Limpar todo histórico\n"
        historico_text += "• `/historico limpar processo` - Limpar apenas processos\n"
        
        historico_text += message_formatter.footer()
        
        await update.message.reply_text(historico_text, parse_mode=ParseMode.MARKDOWN)
        
    except Exception as e:
        logger.error(f"Erro no comando /historico: {e}")
        await update.message.reply_text(
            "⚠️ Erro ao buscar histórico. Tente novamente.",
            parse_mode=ParseMode.MARKDOWN
        )


async def cmd_perfil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /perfil - Ver perfil"""
    await safe_send_typing(update.message.chat)
    
    from services.database_service import db_service
    from services.auth_service import auth_service
    
    user = update.effective_user
    user_id = user.id
    
    # Buscar dados do usuário
    try:
        db_user = db_service.get_or_create_user(user_id, user.username or "User", user.full_name or "User")
        auth_status = "✅ Autenticado" if auth_service.is_authenticated(user_id) else "❌ Não autenticado"
        
        email = "Não cadastrado"
        if db_user and hasattr(db_user, 'email'):
            email = db_user.email or "Não cadastrado"
        
        perfil_text = (
            f"👤 **Meu Perfil**\n\n"
            f"🆔 ID: {user.id}\n"
            f"👤 Nome: {user.full_name}\n"
            f"📧 Email: {email}\n"
            f"🔒 Status: {auth_status}\n\n"
        )
        
        if auth_service.is_authenticated(user_id):
            perfil_text += "✅ Você tem acesso ao Kermartin\n\n"
        
        perfil_text += (
            f"💳 Plano: Gratuito\n"
            f"📊 Consultas este mês: 0"
        )
        
        await update.message.reply_text(perfil_text, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.error(f"Erro ao buscar perfil: {e}")
        await update.message.reply_text(
            f"👤 **Meu Perfil**\n\n"
            f"🆔 ID: {user.id}\n"
            f"👤 Nome: {user.full_name}\n"
            f"@ {user.username or 'N/A'}\n",
            parse_mode=ParseMode.MARKDOWN
        )


async def cmd_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /login - Fazer login em dois passos para acessar Kermartin"""
    await safe_send_typing(update.message.chat)
    
    from services.auth_service import auth_service
    
    user_id = update.effective_user.id
    
    # Iniciar login em dois passos
    sucesso, mensagem = auth_service.iniciar_login(user_id)
    
    # Marcar que está aguardando email
    context.user_data['aguardando_email_login'] = True
    
    await update.message.reply_text(mensagem, parse_mode=ParseMode.MARKDOWN)


async def cmd_recuperar_senha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /recuperar_senha - Recuperar senha usando código"""
    await safe_send_typing(update.message.chat)
    
    from services.auth_service import auth_service
    
    user_id = update.effective_user.id
    args = context.args or []
    
    if len(args) == 0:
        # Gerar código de recuperação
        await update.message.reply_text(
            "🔐 **Recuperação de Senha**\n\n"
            "Para recuperar sua senha, informe seu email cadastrado:\n\n"
            "**Formato:**\n"
            "`/recuperar_senha email@exemplo.com`\n\n"
            "Você receberá um código de 6 dígitos válido por 15 minutos.",
            parse_mode=ParseMode.MARKDOWN
        )
        context.user_data['aguardando_email_recuperacao'] = True
        return
    
    if len(args) == 1:
        # Gerar código para o email informado
        email = args[0]
        sucesso, mensagem, codigo = auth_service.gerar_codigo_recuperacao(email)
        await update.message.reply_text(mensagem, parse_mode=ParseMode.MARKDOWN)
        return
    
    if len(args) >= 2:
        # Usar código para recuperar senha
        codigo = args[0]
        nova_senha = ' '.join(args[1:])
        
        sucesso, mensagem = auth_service.recuperar_senha(codigo, nova_senha)
        await update.message.reply_text(mensagem, parse_mode=ParseMode.MARKDOWN)
        return


async def cmd_trocar_senha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /trocar_senha - Trocar senha (requer senha atual)"""
    await safe_send_typing(update.message.chat)
    
    from services.auth_service import auth_service
    
    user_id = update.effective_user.id
    args = context.args or []
    
    if len(args) < 2:
        await update.message.reply_text(
            "🔐 **Trocar Senha**\n\n"
            "**Formato:**\n"
            "`/trocar_senha senha_atual nova_senha`\n\n"
            "**Exemplo:**\n"
            "`/trocar_senha senha123 novaSenha456`\n\n"
            "⚠️ Você precisa informar sua senha atual para confirmar a troca.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    senha_atual = args[0]
    nova_senha = ' '.join(args[1:])
    
    sucesso, mensagem = auth_service.trocar_senha(user_id, senha_atual, nova_senha)
    await update.message.reply_text(mensagem, parse_mode=ParseMode.MARKDOWN)


async def cmd_comparar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /comparar - Comparar magistrados ou promotores"""
    await safe_send_typing(update.message.chat)
    
    from services.auth_service import auth_service
    from services.kermartin_service import kermartin_service
    from utils.message_formatter import message_formatter
    
    user_id = update.effective_user.id
    
    # Verificar autenticação
    if not auth_service.is_authenticated(user_id):
        await update.message.reply_text(
            auth_service.require_auth_message(),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    args = context.args or []
    
    if len(args) < 3:
        await update.message.reply_text(
            "📊 **Comparar Magistrados/Promotores**\n\n"
            "**Formato:**\n"
            "`/comparar magistrado \"Nome 1\" \"Nome 2\"`\n\n"
            "**Exemplo:**\n"
            "`/comparar magistrado \"Dimas Borges\" \"João Marcos\"`\n\n"
            "💡 Compare estatísticas de dois magistrados ou promotores.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    tipo = args[0].lower()
    nome1 = args[1].strip('"\'')
    nome2 = args[2].strip('"\'')
    
    try:
        if tipo == 'magistrado':
            comparacao = kermartin_service.comparar_magistrados(nome1, nome2)
            
            if not comparacao:
                await update.message.reply_text(
                    "⚠️ Não foi possível comparar os magistrados.\n\n"
                    "Verifique se os nomes estão corretos.",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            stats1 = comparacao['magistrado1']
            stats2 = comparacao['magistrado2']
            
            resposta = message_formatter.header("COMPARAÇÃO DE MAGISTRADOS", "📊")
            
            resposta += f"\n**{stats1['nome']}** vs **{stats2['nome']}**\n\n"
            resposta += message_formatter.SEPARADOR + "\n\n"
            
            resposta += message_formatter.section("Estatísticas Gerais", 
                f"**{stats1['nome']}:**\n"
                f"   • Total de julgados: {stats1['total_julgados']}\n"
                f"   • Taxa de condenação: {stats1['taxa_condenacao']}%\n"
                f"   • Taxa de absolvição: {stats1['taxa_absolvicao']}%\n\n"
                f"**{stats2['nome']}:**\n"
                f"   • Total de julgados: {stats2['total_julgados']}\n"
                f"   • Taxa de condenação: {stats2['taxa_condenacao']}%\n"
                f"   • Taxa de absolvição: {stats2['taxa_absolvicao']}%",
                "📊")
            
            resposta += f"\n{message_formatter.SEPARADOR}\n\n"
            resposta += message_formatter.section("Análise Comparativa",
                f"   • Diferença na taxa de condenação: {comparacao['diferenca_taxa_condenacao']:.1f}%\n"
                f"   • Diferença no total de julgados: {comparacao['diferenca_total']}\n"
                f"   • Mais condenador: {comparacao['mais_condenador']}\n"
                f"   • Mais julgados: {comparacao['mais_julgados']}",
                "💡")
            
            resposta += message_formatter.footer()
            
            await update.message.reply_text(resposta, parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text(
                "⚠️ Tipo de comparação não suportado.\n\n"
                "Use: `/comparar magistrado \"Nome 1\" \"Nome 2\"`",
                parse_mode=ParseMode.MARKDOWN
            )
            
    except Exception as e:
        logger.error(f"Erro no comando /comparar: {e}")
        await update.message.reply_text(
            "⚠️ Erro ao comparar. Tente novamente.",
            parse_mode=ParseMode.MARKDOWN
        )


async def cmd_padroes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /padroes - Análise de padrões de julgamento"""
    await safe_send_typing(update.message.chat)
    
    from services.auth_service import auth_service
    from services.kermartin_service import kermartin_service
    from utils.message_formatter import message_formatter
    
    user_id = update.effective_user.id
    
    # Verificar autenticação
    if not auth_service.is_authenticated(user_id):
        await update.message.reply_text(
            auth_service.require_auth_message(),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    args = context.args or []
    
    if len(args) < 2:
        await update.message.reply_text(
            "🔍 **Análise de Padrões de Julgamento**\n\n"
            "**Formato:**\n"
            "`/padroes magistrado \"Nome\"`\n"
            "`/padroes crime \"Tipo de Crime\"`\n"
            "`/padroes comarca \"Nome da Comarca\"`\n\n"
            "**Exemplos:**\n"
            "`/padroes magistrado \"Dimas Borges\"`\n"
            "`/padroes crime \"Homicídio qualificado\"`\n"
            "`/padroes comarca \"Uberlândia\"`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    tipo = args[0].lower()
    valor = ' '.join(args[1:]).strip('"\'')
    
    try:
        padroes = kermartin_service.analisar_padroes(tipo, valor)
        
        if not padroes:
            await update.message.reply_text(
                "⚠️ Não foi possível analisar padrões.\n\n"
                "Verifique se os dados estão corretos.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        resposta = message_formatter.header("ANÁLISE DE PADRÕES", "🔍")
        
        resposta += f"\n**Tipo:** {tipo.upper()}\n"
        resposta += f"**Valor:** {valor}\n\n"
        resposta += message_formatter.SEPARADOR + "\n\n"
        
        resposta += message_formatter.section("Estatísticas",
            f"   • Total de casos: {padroes['total_casos']}\n"
            f"   • Taxa de condenação: {padroes['taxa_condenacao_geral']:.1f}%\n"
            f"   • Taxa de absolvição: {padroes['taxa_absolvicao_geral']:.1f}%",
            "📊")
        
        if padroes.get('crimes_frequentes'):
            resposta += f"\n{message_formatter.SEPARADOR}\n\n"
            resposta += message_formatter.section("Crimes Mais Frequentes",
                "\n".join([f"   • {crime} ({count} casos)" for crime, count in padroes['crimes_frequentes']]),
                "📋")
        
        resposta += f"\n{message_formatter.SEPARADOR}\n\n"
        
        tendencia_text = {
            'condenador': '🔴 Tendência a condenar (taxa > 70%)',
            'absolvedor': '🟢 Tendência a absolver (taxa > 70%)',
            'equilibrado': '⚖️ Padrão equilibrado de decisões'
        }
        
        resposta += message_formatter.section("Tendência Identificada",
            tendencia_text.get(padroes['tendencia'], 'N/A'),
            "💡")
        
        resposta += message_formatter.footer()
        
        await update.message.reply_text(resposta, parse_mode=ParseMode.MARKDOWN)
        
    except Exception as e:
        logger.error(f"Erro no comando /padroes: {e}")
        await update.message.reply_text(
            "⚠️ Erro ao analisar padrões. Tente novamente.",
            parse_mode=ParseMode.MARKDOWN
        )


async def cmd_logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /logout - Fazer logout"""
    await safe_send_typing(update.message.chat)
    
    from services.auth_service import auth_service
    
    user_id = update.effective_user.id
    sucesso, mensagem = auth_service.logout(user_id)
    
    await update.message.reply_text(mensagem, parse_mode=ParseMode.MARKDOWN)


async def cmd_cadastrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /cadastrar - Cadastrar email e senha"""
    await safe_send_typing(update.message.chat)
    
    from services.auth_service import auth_service
    
    user_id = update.effective_user.id
    
    # Verificar argumentos
    args = context.args
    
    if not args or len(args) < 2:
        await update.message.reply_text(
            "📝 **Cadastro de Email e Senha**\n\n"
            "**Formato:**\n"
            "`/cadastrar email@exemplo.com senha`\n\n"
            "**Exemplo:**\n"
            "`/cadastrar usuario@exemplo.com minhasenha123`\n\n"
            "💡 Após cadastrar, use `/login` para acessar o Kermartin.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    email = args[0]
    password = args[1]
    
    # Cadastrar
    sucesso, mensagem = auth_service.register_user_email(user_id, email, password)
    
    await update.message.reply_text(mensagem, parse_mode=ParseMode.MARKDOWN)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para callbacks dos botões inline"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    try:
        # Importar serviço de alertas
        from services.alertas_service import alertas_service
        from services.database_service import db_service
        
        # Buscar ou criar usuário (não crítico)
        user = db_service.get_or_create_user(
            user_id,
            update.effective_user.username or "User",
            update.effective_user.full_name or "User"
        )
        
        if not user:
            # Banco não disponível - continuar sem salvar preferências
            logger.warning("Banco de dados não disponível - preferências não serão salvas")
        
        if query.data.startswith("alerta_"):
            # Configurar alerta via canal selecionado
            canal = query.data.split("_")[1]
            
            # Mapear valores
            canal_map = {
                "email": "email",
                "telegram": "telegram",
                "custom": "telegram"  # default para custom
            }
            canal_preferido = canal_map.get(canal, "telegram")
            
            # Salvar preferência no banco (se disponível)
            sucesso = False
            if user:
                sucesso = alertas_service.update_alert_channel(user.id, canal_preferido)
            else:
                logger.warning("Banco não disponível - configuração não salva")
            
            if sucesso:
                logger.info(f"Usuário {user_id} configurou alertas via {canal_preferido}")
                emoji = "📧" if canal_preferido == "email" else "📱"
                
                await query.edit_message_text(
                    f"✅ **Alerta configurado!**\n\n"
                    f"{emoji} Você receberá notificações via {canal_preferido.upper()}\n\n"
                    f"💡 Use /alerta novamente para ajustar o intervalo."
                )
            else:
                await query.edit_message_text(
                    "⚠️ Erro ao salvar preferência. Tente novamente."
                )
        
        elif query.data.startswith("intervalo_"):
            # Configurar intervalo de alertas
            try:
                dias = int(query.data.split("_")[1])
                
                # Validar intervalo
                if dias not in [1, 3, 7]:
                    dias = 3  # default
                
                # Salvar intervalo no banco (se disponível)
                sucesso = False
                if user:
                    sucesso = alertas_service.update_alert_interval(user.id, dias)
                else:
                    logger.warning("Banco não disponível - intervalo não salvo")
                
                if sucesso:
                    logger.info(f"Usuário {user_id} configurou intervalo de {dias} dias")
                    
                    await query.edit_message_text(
                        f"✅ **Intervalo configurado!**\n\n"
                        f"⏰ Você receberá alertas **{dias} dias** antes do vencimento.\n\n"
                        f"📋 Configuração completa!\n"
                        f"💡 Use /alerta para alterar novamente."
                    )
                else:
                    await query.edit_message_text(
                        "⚠️ Erro ao salvar intervalo. Tente novamente."
                    )
            except ValueError:
                await query.edit_message_text(
                    "⚠️ Intervalo inválido. Use /alerta novamente."
                )
        
        elif query.data.startswith("config_"):
            # Configurações gerais
            config_type = query.data.split("_")[1]
            
            if config_type == "notif":
                await query.edit_message_text(
                    "🔔 **Configurações de Notificações**\n\n"
                    "Escolha a frequência:\n\n"
                    "📱 Todos os alertas\n"
                    "🔴 Apenas urgentes\n"
                    "📅 Diário resumido\n"
                )
            
            elif config_type == "email":
                await query.edit_message_text(
                    "📧 **Configuração de Email**\n\n"
                    "Digite seu email no formato:\n"
                    "email@exemplo.com\n\n"
                    "💡 Enviaremos seus alertas por email."
                )
            
            elif config_type == "telegram":
                await query.edit_message_text(
                    "📱 **Notificações Telegram**\n\n"
                    "✅ Ativadas\n\n"
                    "Você receberá alertas diretamente aqui no Telegram."
                )
            
            elif config_type == "idioma":
                await query.edit_message_text(
                    "🌐 **Idioma**\n\n"
                    "✅ Português (BR)\n\n"
                    "Sempre falaremos em português brasileiro!"
                )
        
        else:
            await query.edit_message_text(
                "⚙️ Opção reconhecida! Em breve teremos mais funcionalidades."
            )
            
    except Exception as e:
        logger.error(f"Erro ao processar callback: {e}")
        await query.edit_message_text(
            "⚠️ Erro ao processar configuração. Tente novamente."
        )


async def register_bot_commands(application: Application):
    """
    Registra comandos na API do Telegram para aparecerem no menu de comandos
    """
    try:
        commands = [
            BotCommand("start", "Reiniciar o bot"),
            BotCommand("help", "Ver ajuda completa"),
            BotCommand("menu", "Menu principal interativo"),
            BotCommand("processo", "Consultar processo (API CNJ + Kermartin)"),
            BotCommand("buscar", "Buscar jurisprudência"),
            BotCommand("magistrado", "Buscar perfil de magistrado"),
            BotCommand("promotor", "Buscar perfil de promotor"),
            BotCommand("comarca", "Processos por comarca"),
            BotCommand("prazos", "Ver prazos processuais pendentes"),
            BotCommand("alerta", "Configurar alertas"),
            BotCommand("historico", "Histórico de consultas"),
            BotCommand("estatisticas", "Estatísticas gerais do Kermartin"),
            BotCommand("perfil", "Meu perfil"),
            BotCommand("config", "Configurações"),
            BotCommand("cache", "Estatísticas de cache e memória"),
            BotCommand("status", "Status de autenticação"),
            BotCommand("login", "Fazer login para acessar Kermartin"),
            BotCommand("logout", "Fazer logout"),
            BotCommand("cadastrar", "Cadastrar email e senha"),
            BotCommand("recuperar_senha", "Recuperar senha usando código"),
            BotCommand("trocar_senha", "Trocar senha"),
            BotCommand("comparar", "Comparar magistrados ou promotores"),
            BotCommand("padroes", "Análise de padrões de julgamento"),
        ]
        
        await application.bot.set_my_commands(commands)
        logger.info(f"✅ {len(commands)} comandos registrados na API do Telegram")
        return True
    except Exception as e:
        logger.error(f"⚠️ Erro ao registrar comandos na API do Telegram: {e}")
        logger.warning("Os comandos funcionarão mesmo assim, mas podem não aparecer no menu")
        return False


def register_command_handlers(application: Application):
    """Registra todos os command handlers"""
    application.add_handler(CommandHandler("help", cmd_help))
    application.add_handler(CommandHandler("menu", cmd_menu))
    application.add_handler(CommandHandler("buscar", cmd_buscar))
    application.add_handler(CommandHandler("prazos", cmd_prazos))
    application.add_handler(CommandHandler("alerta", cmd_alerta))
    application.add_handler(CommandHandler("processo", cmd_processo))
    application.add_handler(CommandHandler("magistrado", cmd_magistrado))
    application.add_handler(CommandHandler("promotor", cmd_promotor))
    application.add_handler(CommandHandler("comarca", cmd_comarca))
    application.add_handler(CommandHandler("config", cmd_config))
    application.add_handler(CommandHandler("perfil", cmd_perfil))
    application.add_handler(CommandHandler("historico", cmd_historico))
    application.add_handler(CommandHandler("estatisticas", cmd_estatisticas))
    application.add_handler(CommandHandler("cache", cmd_cache_stats))
    application.add_handler(CommandHandler("status", cmd_status))
    application.add_handler(CommandHandler("login", cmd_login))
    application.add_handler(CommandHandler("logout", cmd_logout))
    application.add_handler(CommandHandler("cadastrar", cmd_cadastrar))
    application.add_handler(CommandHandler("recuperar_senha", cmd_recuperar_senha))
    application.add_handler(CommandHandler("trocar_senha", cmd_trocar_senha))
    application.add_handler(CommandHandler("comparar", cmd_comparar))
    application.add_handler(CommandHandler("padroes", cmd_padroes))
    
    # Callback handler para botões inline
    application.add_handler(CallbackQueryHandler(button_callback))

