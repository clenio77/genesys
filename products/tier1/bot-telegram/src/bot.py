"""
Bot principal do Telegram Jurídico
"""

import asyncio
import sys
from pathlib import Path

# Adiciona o diretório pai ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.config.settings import settings
from shared.utils.logger import bot_telegram_logger as logger
from handlers.commands import register_command_handlers
from handlers.messages import handle_message
from services.database_service import db_service


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para comando /start"""
    
    # Criar ou buscar usuário no banco (não crítico - pode retornar None)
    try:
        user_id = update.effective_user.id
        username = update.effective_user.username or "Unknown"
        full_name = update.effective_user.full_name or "User"
        
        user = db_service.get_or_create_user(user_id, username, full_name)
        if user:
            logger.info(f"Usuário {user_id} iniciou o bot")
        else:
            logger.info(f"Usuário {user_id} iniciou o bot (sem banco de dados)")
        
    except Exception as e:
        logger.warning(f"Erro ao criar/buscar usuário (não crítico): {e}")
    
    welcome_message = """🤖 **Bem-vindo ao Genesys Bot Jurídico!**\n\n
Posso ajudá-lo com:\n
• 🧠 Consultas jurídicas com IA\n
• 🔍 Busca de jurisprudência\n
• 📅 Controle de prazos processuais\n
• 🔔 Alertas automáticos\n
• ⚖️ Consulta de processos (API CNJ + base local)\n
• 👨‍⚖️ Perfis de magistrados\n\n
**Comandos principais:**\n
/start - Reiniciar o bot
/help - Ver ajuda completa
/buscar - Buscar jurisprudência
/prazos - Ver prazos pendentes
/alerta - Configurar alertas
/processo - Consultar processo
/magistrado - Buscar magistrado\n\n
💬 Envie uma mensagem para conversar comigo!"""
    
    await update.message.reply_text(
        welcome_message,
        parse_mode=ParseMode.MARKDOWN
    )


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para mensagens de texto"""
    await handle_message(update, context)


def create_application() -> Application:
    """Cria e configura a aplicação do Telegram"""
    
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN não configurado!")
        sys.exit(1)
    
    # Criar aplicação
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    # Registrar command handlers
    application.add_handler(CommandHandler("start", start))
    register_command_handlers(application)
    
    # Registrar message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    return application


async def main():
    """Função principal"""
    logger.info("Iniciando Bot de Telegram Jurídico...")
    
    application = create_application()
    
    # Registrar comandos na API do Telegram (para aparecerem no menu)
    try:
        from handlers.commands import register_bot_commands
        await register_bot_commands(application)
    except Exception as e:
        logger.warning(f"Erro ao registrar comandos na API: {e}")
    
    # Iniciar bot
    logger.info("Bot iniciado com sucesso!")
    logger.info("🔄 Bot rodando... Aguardando mensagens no Telegram...")
    
    await application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )


if __name__ == "__main__":
    # Configurar event loop policy
    import sys
    
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot interrompido pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        raise

