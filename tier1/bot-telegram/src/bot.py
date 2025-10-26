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

from shared.config.settings import settings
from shared.utils.logger import bot_telegram_logger as logger
from .handlers.commands import register_command_handlers
from .handlers.messages import handle_message


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para comando /start"""
    await update.message.reply_text(
        "🤖 **Bem-vindo ao Genesys Bot Jurídico!**\n\n"
        "Comandos disponíveis:\n"
        "/start - Iniciar o bot\n"
        "/help - Ver ajuda\n"
        "/buscar - Buscar jurisprudência\n"
        "/prazos - Ver prazos pendentes\n"
        "/alerta - Configurar alertas\n\n"
        "Envie uma mensagem para conversar comigo sobre questões jurídicas!",
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
    
    # Iniciar bot
    logger.info("Bot iniciado com sucesso!")
    await application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )


if __name__ == "__main__":
    asyncio.run(main())

