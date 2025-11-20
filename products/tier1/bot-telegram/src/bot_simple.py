"""
Bot simplificado sem problemas de event loop
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from shared.config.settings import settings
from shared.utils.logger import bot_telegram_logger as logger


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para /start"""
    await update.message.reply_text(
        "🤖 **Bem-vindo ao Genesys Bot Jurídico!**\n\n"
        "Posso ajudá-lo com consultas jurídicas.\n\n"
        "Comandos:\n"
        "/start - Este comando\n"
        "/help - Ver ajuda completa\n\n"
        "Envie uma mensagem para conversar!",
        parse_mode="Markdown"
    )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para /help"""
    await update.message.reply_text(
        "📚 **Comandos Disponíveis:**\n\n"
        "/start - Reiniciar bot\n"
        "/help - Ver esta ajuda\n"
        "/buscar - Buscar jurisprudência\n"
        "/prazos - Ver prazos pendentes\n"
        "/alerta - Configurar alertas\n\n"
        "💬 Você também pode enviar mensagens em linguagem natural!",
        parse_mode="Markdown"
    )


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para mensagens de texto"""
    user_message = update.message.text
    user = update.effective_user
    
    logger.info(f"Usuário {user.id} ({user.username}): {user_message}")
    
    # Resposta simples
    response = f"✅ Recebi sua mensagem: '{user_message}'\n\n"
    response += "🤖 Em breve implementarei respostas inteligentes com IA!\n\n"
    response += "Use /help para ver comandos disponíveis."
    
    await update.message.reply_text(response)


def main():
    """Função principal"""
    logger.info("🤖 Iniciando Bot de Telegram Jurídico...")
    
    if not settings.TELEGRAM_BOT_TOKEN or settings.TELEGRAM_BOT_TOKEN == "your_telegram_bot_token_here":
        logger.error("❌ TELEGRAM_BOT_TOKEN não configurado!")
        return
    
    # Criar aplicação
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    # Registrar handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    logger.info("✅ Bot iniciado! Aguardando mensagens...")
    
    # Rodar
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()

