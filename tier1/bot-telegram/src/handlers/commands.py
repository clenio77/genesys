"""
Handlers para comandos do bot
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode

from shared.utils.logger import bot_telegram_logger as logger


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help"""
    help_text = """
📚 **Comandos Disponíveis:**

/start - Reiniciar o bot
/help - Ver esta ajuda
/buscar - Buscar jurisprudência
/prazos - Ver prazos processuais pendentes
/alerta - Configurar alertas
/processo - Consultar status de processo
/config - Configurações
/perfil - Meu perfil

💡 **Dica:** Você também pode fazer perguntas em linguagem natural e eu tentarei ajudar!
"""
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)


async def cmd_buscar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /buscar - Buscar jurisprudência"""
    await update.message.reply_text(
        "🔍 **Busca de Jurisprudência**\n\n"
        "Envie o tema ou questão jurídica que deseja buscar.\n"
        "Exemplo: 'indenização por danos morais'\n\n"
        "💡 Eu buscarei em nossa base de decisões e te mostrarei os resultados mais relevantes!",
        parse_mode=ParseMode.MARKDOWN
    )


async def cmd_prazos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /prazos - Listar prazos pendentes"""
    # TODO: Implementar busca de prazos do banco de dados
    await update.message.reply_text(
        "📅 **Seus Prazos Processuais**\n\n"
        "Você não possui prazos pendentes no momento.\n\n"
        "Use /alerta para configurar alertas automáticos!",
        parse_mode=ParseMode.MARKDOWN
    )


async def cmd_alerta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /alerta - Configurar alertas"""
    keyboard = [
        [
            InlineKeyboardButton("📧 Via Email", callback_data="alerta_email"),
            InlineKeyboardButton("📱 Via Telegram", callback_data="alerta_telegram")
        ],
        [
            InlineKeyboardButton("⏰ Intervalo 7 dias", callback_data="intervalo_7"),
            InlineKeyboardButton("⏰ Intervalo 3 dias", callback_data="intervalo_3"),
            InlineKeyboardButton("⏰ Intervalo 1 dia", callback_data="intervalo_1")
        ],
        [
            InlineKeyboardButton("✏️ Personalizado", callback_data="alerta_custom")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "⚙️ **Configuração de Alertas**\n\n"
        "Escolha como deseja receber seus alertas de prazos:",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )


async def cmd_processo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /processo - Consultar processo"""
    await update.message.reply_text(
        "⚖️ **Consulta de Processo**\n\n"
        "Envie o número do processo no formato:\n"
        "NNNNNNNN-DD.AAAA.J.TR.OOOO (ex: 0001234-56.2023.8.26.0100)\n\n"
        "💡 Eu consultarei o status e te mostrarei as movimentações!",
        parse_mode=ParseMode.MARKDOWN
    )


async def cmd_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /config - Configurações"""
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


async def cmd_perfil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /perfil - Ver perfil"""
    user = update.effective_user
    
    await update.message.reply_text(
        f"👤 **Meu Perfil**\n\n"
        f"🆔 ID: {user.id}\n"
        f"👤 Nome: {user.full_name}\n"
        f"@ {user.username or 'N/A'}\n\n"
        f"💳 Plano: Gratuito\n"
        f"📊 Consultas este mês: 0\n",
        parse_mode=ParseMode.MARKDOWN
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para callbacks dos botões inline"""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("alerta_"):
        # Configurar alerta via canal selecionado
        canal = query.data.split("_")[1]
        await query.edit_message_text(
            f"✅ Alerta configurado para receber via {canal.upper()}!"
        )
    
    elif query.data.startswith("intervalo_"):
        # Configurar intervalo de alertas
        dias = query.data.split("_")[1]
        await query.edit_message_text(
            f"✅ Alertas configurados para {dias} dias antes do vencimento!"
        )


def register_command_handlers(application: Application):
    """Registra todos os command handlers"""
    application.add_handler(CommandHandler("help", cmd_help))
    application.add_handler(CommandHandler("buscar", cmd_buscar))
    application.add_handler(CommandHandler("prazos", cmd_prazos))
    application.add_handler(CommandHandler("alerta", cmd_alerta))
    application.add_handler(CommandHandler("processo", cmd_processo))
    application.add_handler(CommandHandler("config", cmd_config))
    application.add_handler(CommandHandler("perfil", cmd_perfil))
    
    # Callback handler para botões inline
    application.add_handler(CallbackQueryHandler(button_callback))

