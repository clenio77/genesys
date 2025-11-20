"""
Bot com IA integrada para respostas inteligentes
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Carregar variáveis de ambiente do arquivo .env ANTES de importar settings
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import error as telegram_error
from shared.config.settings import settings
from shared.utils.logger import bot_telegram_logger as logger

# Importar serviço de IA
from services.ia_service import ai_service
from services.database_service import db_service


# Importar handlers completos com indicadores UX
from handlers.messages import handle_message as text_handler


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para /start com indicador de digitação"""
    # Mostrar indicador de digitação (de forma segura)
    try:
        await update.message.chat.send_action("typing")
    except Exception:
        pass  # Ignorar timeouts - não é crítico
    
    # Criar/buscar usuário
    try:
        user = update.effective_user
        db_service.get_or_create_user(user.id, user.username or "User", user.full_name or "User")
    except:
        pass
    
    await update.message.reply_text(
        "🤖 **Bem-vindo ao Genesys Bot Jurídico!**\n\n"
        "Posso ajudá-lo com:\n"
        "• 🧠 Consultas jurídicas com IA\n"
        "• 🔍 Busca de jurisprudência\n"
        "• 📅 Controle de prazos processuais\n"
        "• 🔔 Alertas automáticos\n"
        "• ⚖️ Consulta de processos (API CNJ + base local)\n"
        "• 👨‍⚖️ Perfis de magistrados\n\n"
        "**Comandos principais:**\n"
        "• /start - Reiniciar bot\n"
        "• /help - Ver ajuda completa\n"
        "• /buscar - Buscar jurisprudência\n"
        "• /prazos - Ver prazos pendentes\n"
        "• /alerta - Configurar alertas\n"
        "• /processo - Consultar processo\n"
        "• /magistrado - Buscar magistrado\n"
        "• /perfil - Meu perfil\n\n"
        "🔐 **Autenticação (Kermartin):**\n"
        "• /login - Fazer login para acessar Kermartin\n"
        "• /logout - Fazer logout\n"
        "• /cadastrar - Cadastrar email e senha\n\n"
        "💡 **Dica:** Use /login para acessar dados do Kermartin!\n\n"
        "💬 Envie uma mensagem para conversar com IA!",
        parse_mode="Markdown"
    )


def main():
    """Função principal"""
    logger.info("🤖 Iniciando Bot de Telegram com IA...")
    
    if not settings.TELEGRAM_BOT_TOKEN or settings.TELEGRAM_BOT_TOKEN == "your_telegram_bot_token_here":
        logger.error("❌ TELEGRAM_BOT_TOKEN não configurado!")
        return
    
    # Criar aplicação
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    # Registrar comando /start com indicador UX
    application.add_handler(CommandHandler("start", start_handler))
    logger.info("✅ Comando /start registrado")
    
    # Importar e registrar todos os outros comandos
    try:
        from handlers.commands import register_command_handlers, register_bot_commands
        register_command_handlers(application)
        logger.info("✅ Todos os comandos registrados")
    except Exception as e:
        logger.error(f"Erro ao registrar comandos: {e}")
    
    # Message handler deve vir por último
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    logger.info("✅ Handler de mensagens registrado")
    
    # Registrar comandos na API do Telegram após inicialização
    async def post_init(app: Application) -> None:
        """Executado após inicialização do bot"""
        try:
            await register_bot_commands(app)
        except Exception as e:
            logger.warning(f"Erro ao registrar comandos na API: {e}")
    
    application.post_init = post_init
    
    logger.info("✅ Bot com IA iniciado! Aguardando mensagens...")
    
    # Rodar com tratamento de erros de rede
    try:
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
            stop_signals=None  # Não parar em sinais, apenas Ctrl+C
        )
    except telegram_error.NetworkError as e:
        logger.error(f"❌ Erro de rede ao conectar com Telegram: {e}")
        logger.error("💡 Verifique sua conexão com a internet e tente novamente")
        print("\n❌ Erro de Conexão!")
        print("O bot não conseguiu conectar à API do Telegram.")
        print("\nPossíveis causas:")
        print("  • Sem conexão com a internet")
        print("  • Problema temporário de DNS")
        print("  • Firewall bloqueando a conexão")
        print("\n💡 Tente novamente em alguns segundos.")
    except KeyboardInterrupt:
        logger.info("🛑 Bot interrompido pelo usuário")
        print("\n✅ Bot encerrado.")
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {e}")
        raise


if __name__ == "__main__":
    main()

