"""
Handlers para mensagens de texto do bot
"""

from telegram import Update
from telegram.ext import ContextTypes

from shared.utils.logger import bot_telegram_logger as logger


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler principal para mensagens de texto
    
    Processa mensagens em linguagem natural e usa IA para gerar respostas
    """
    user_message = update.message.text
    user_id = update.effective_user.id
    
    logger.info(f"Usuário {user_id} enviou: {user_message}")
    
    # TODO: Implementar integração com RAG System e LLM
    # Por enquanto, retorna uma mensagem padrão
    
    # Analisar mensagem
    if any(palavra in user_message.lower() for palavra in ['jurisprudência', 'decisão', 'acórdão', 'precedente']):
        response = "🔍 **Busca de Jurisprudência**\n\n" \
                  "Você está buscando jurisprudência! 🤖\n\n" \
                  "Em breve implementarei a busca semântica avançada.\n" \
                  "Por enquanto, use o comando /buscar para mais informações!"
    
    elif any(palavra in user_message.lower() for palavra in ['prazo', 'vencimento', 'processo']):
        response = "📅 **Prazos Processuais**\n\n" \
                  "Você está perguntando sobre prazos! 🗓️\n\n" \
                  "Use o comando /prazos para ver seus prazos pendentes\n" \
                  "ou /alerta para configurar alertas automáticos!"
    
    elif any(palavra in user_message.lower() for palavra in ['contato', 'falar', 'suporte', 'ajuda']):
        response = "💬 **Suporte Genesys**\n\n" \
                  "Para falar com nossa equipe:\n" \
                  "📧 Email: contato@genesys-tecnologia.com.br\n" \
                  "📱 WhatsApp: +55 34 99826-4603\n" \
                  "🌐 Site: https://genesys-tecnologia.com.br"
    
    else:
        response = "🤖 **Genesys IA Jurídica**\n\n" \
                  "Olá! Sou um assistente jurídico inteligente. ⚖️\n\n" \
                  "Posso ajudar com:\n" \
                  "• Busca de jurisprudência\n" \
                  "• Consulta de prazos processuais\n" \
                  "• Análise de processos\n" \
                  "• Alertas e notificações\n\n" \
                  "Digite /help para ver todos os comandos disponíveis!"
    
    await update.message.reply_text(response)

