"""
Handlers para mensagens de texto do bot
"""

import sys
import traceback
from pathlib import Path

# Adiciona o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from shared.utils.logger import bot_telegram_logger as logger
from shared.utils.text_sanitizer import sanitize_text
from services.ia_service import ai_service
from services.database_service import db_service


def split_message(text: str, max_length: int = 3900) -> list:
    """
    Divide mensagem longa em múltiplas partes (mensagens separadas)
    Tenta cortar em pontos lógicos (fim de parágrafo, frase, etc.)
    
    Args:
        text: Texto completo a ser dividido
        max_length: Tamanho máximo por parte (3900 para margem de segurança)
    
    Returns:
        Lista de strings, cada uma será enviada como mensagem separada
    """
    if not text:
        return [""]
    
    # Se cabe em uma mensagem, retorna sem dividir
    if len(text) <= max_length:
        return [text]
    
    parts = []
    current_pos = 0
    text_len = len(text)
    
    while current_pos < text_len:
        remaining = text_len - current_pos
        
        # Se o que resta cabe em uma mensagem, pega tudo
        if remaining <= max_length:
            parts.append(text[current_pos:].strip())
            break
        
        # Buscar melhor ponto de corte dentro do limite
        search_end = current_pos + max_length - 100  # Margem para cabeçalho
        chunk = text[current_pos:search_end]
        
        # Ordem de preferência para pontos de corte (mais lógicos primeiro)
        cut_pos = -1
        cut_offset = 0
        
        # 1. Parágrafo duplo (melhor opção)
        pos = chunk.rfind("\n\n")
        if pos > max_length * 0.4:  # Só se não for muito no início
            cut_pos = pos
            cut_offset = 2
        # 2. Quebra de linha simples
        elif chunk.rfind("\n") > max_length * 0.5:
            pos = chunk.rfind("\n")
            cut_pos = pos
            cut_offset = 1
        # 3. Fim de frase (ponto + espaço)
        elif chunk.rfind(". ") > max_length * 0.5:
            pos = chunk.rfind(". ")
            cut_pos = pos
            cut_offset = 2
        # 4. Qualquer ponto
        elif chunk.rfind(".") > max_length * 0.6:
            pos = chunk.rfind(".")
            cut_pos = pos
            cut_offset = 1
        # 5. Vírgula
        elif chunk.rfind(", ") > max_length * 0.7:
            pos = chunk.rfind(", ")
            cut_pos = pos
            cut_offset = 2
        # 6. Último recurso: corta no limite
        else:
            cut_pos = max_length - 100
            cut_offset = 0
        
        # Extrair esta parte
        end_pos = current_pos + cut_pos + cut_offset
        part = text[current_pos:end_pos].strip()
        
        if part:  # Só adiciona se não estiver vazio
            parts.append(part)
        
        current_pos = end_pos
        
        # Proteção contra loop infinito
        if cut_pos <= 0:
            # Força corte
            parts.append(text[current_pos:current_pos + max_length - 100].strip())
            current_pos += max_length - 100
    
    # Se dividiu em múltiplas partes, adiciona numeração
    if len(parts) > 1:
        numbered = []
        total = len(parts)
        for i, part in enumerate(parts, 1):
            header = f"📄 Parte {i}/{total}\n\n"
            numbered.append(header + part)
        return numbered
    
    return parts


async def safe_reply_text(update: Update, text: str, use_markdown: bool = True):
    """
    Envia mensagem de texto com tratamento de erros de parsing
    Se a mensagem for muito longa, divide em múltiplas mensagens separadas
    Tenta Markdown primeiro, depois HTML, depois texto plano
    
    Args:
        update: Update do Telegram
        text: Texto a ser enviado
        use_markdown: Se deve tentar usar Markdown
    """
    # Dividir em partes se necessário
    parts = split_message(text)
    total_parts = len(parts)
    
    logger.info(f"📤 Enviando mensagem em {total_parts} parte(s)")
    
    for i, part in enumerate(parts, 1):
        logger.debug(f"Enviando parte {i}/{total_parts} ({len(part)} caracteres)")
        
        if use_markdown:
            try:
                # Tenta enviar com Markdown
                sanitized = sanitize_text(part)
                await update.message.reply_text(sanitized, parse_mode="Markdown")
                logger.debug(f"✅ Parte {i}/{total_parts} enviada com Markdown")
                continue
            except Exception as e:
                logger.warning(f"Erro ao enviar parte {i}/{total_parts} com Markdown: {e}. Tentando HTML...")
                try:
                    # Tenta HTML
                    await update.message.reply_text(part, parse_mode="HTML")
                    logger.debug(f"✅ Parte {i}/{total_parts} enviada com HTML")
                    continue
                except Exception as e2:
                    logger.warning(f"Erro ao enviar parte {i}/{total_parts} com HTML: {e2}. Enviando como texto plano...")
        
        # Fallback para texto plano
        try:
            await update.message.reply_text(part, parse_mode=None)
            logger.debug(f"✅ Parte {i}/{total_parts} enviada como texto plano")
        except Exception as e3:
            logger.error(f"❌ Erro ao enviar parte {i}/{total_parts} como texto plano: {e3}")
            
            # Último recurso: truncar esta parte drasticamente
            if len(part) > 3000:
                truncated = part[:3000] + "\n\n⚠️ ... (mensagem muito longa, parte truncada)"
                try:
                    await update.message.reply_text(truncated, parse_mode=None)
                    logger.warning(f"⚠️ Parte {i}/{total_parts} foi truncada")
                except Exception:
                    logger.error(f"❌ Falha total ao enviar parte {i}/{total_parts}")
    
    logger.info(f"✅ Mensagem completa enviada ({total_parts} parte(s))")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler principal para mensagens de texto
    
    Processa mensagens em linguagem natural e usa IA para gerar respostas
    """
    user_message = update.message.text
    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"
    full_name = update.effective_user.full_name or "User"
    
    logger.info(f"Usuário {user_id} ({username}) enviou: {user_message}")
    
    # Processar login em dois passos
    if context.user_data.get('aguardando_email_login', False):
        from services.auth_service import auth_service
        
        # Verificar se é email válido
        if '@' in user_message:
            sucesso, mensagem = auth_service.processar_email_login(user_id, user_message)
            await safe_reply_text(update, mensagem, use_markdown=True)
            
            if sucesso:
                context.user_data['aguardando_email_login'] = False
                context.user_data['aguardando_senha_login'] = True
            else:
                context.user_data['aguardando_email_login'] = False
            return
        else:
            await safe_reply_text(
                update,
                "⚠️ Por favor, informe um email válido (ex: `usuario@exemplo.com`)",
                use_markdown=True
            )
            return
    
    # Processar senha no login em dois passos
    if context.user_data.get('aguardando_senha_login', False):
        from services.auth_service import auth_service
        
        sucesso, mensagem = auth_service.completar_login(user_id, user_message)
        await safe_reply_text(update, mensagem, use_markdown=True)
        
        context.user_data['aguardando_senha_login'] = False
        return
    
    # Processar email para recuperação de senha
    if context.user_data.get('aguardando_email_recuperacao', False):
        from services.auth_service import auth_service
        
        if '@' in user_message:
            sucesso, mensagem, codigo = auth_service.gerar_codigo_recuperacao(user_message)
            await safe_reply_text(update, mensagem, use_markdown=True)
        else:
            await safe_reply_text(
                update,
                "⚠️ Por favor, informe um email válido (ex: `usuario@exemplo.com`)",
                use_markdown=True
            )
        
        context.user_data['aguardando_email_recuperacao'] = False
        return
    
    # Mostrar indicador de digitação (de forma segura - não crítico se falhar)
    try:
        await update.message.chat.send_action("typing")
        logger.debug("✅ Indicador de digitação enviado")
    except Exception as e:
        # Ignorar timeouts - não é crítico se falhar
        logger.debug(f"Erro ao enviar indicador de digitação (ignorando): {type(e).__name__}")
        pass
    
    # Verificar se está aguardando número de processo
    if context.user_data.get('aguardando_processo', False):
        try:
            from services.cnj_service import cnj_service
            
            # Limpar flag
            context.user_data['aguardando_processo'] = False
            
            # Mensagem de status
            logger.info("📝 Consultando processo na API CNJ...")
            status_msg = await update.message.reply_text("🔍 *Consultando processo...*", parse_mode="Markdown")
            
            # Consultar processo (com fallback automático)
            dados = cnj_service.consultar_processo(user_message, telegram_id=update.effective_user.id)
            
            # Se retornou erro mas não é None, pode ter sido encontrado em outra fonte
            if dados and not dados.get('erro'):
                # Formatar resposta
                resposta = cnj_service.formatar_resposta_processo(dados)
            elif dados and dados.get('erro'):
                # Processo não encontrado - informar que será coletado pelo Kermartin
                erro_msg = dados.get('erro', 'Processo não encontrado')
                resposta = f"""⚠️ **Processo não encontrado**

O processo `{user_message}` não foi encontrado nas fontes disponíveis:
• Base de dados local (Kermartin)
• API Pública do CNJ

**O que acontece agora?**

💡 Este processo será coletado automaticamente pelo sistema **Kermartin** em breve.
Você receberá uma notificação quando os dados estiverem disponíveis.

**Para acelerar a coleta:**
• Use o sistema Kermartin para adicionar processos à fila de coleta
• Processos novos são coletados automaticamente em até 24 horas

**Verifique também:**
• Se o número do processo está correto
• Se o processo existe no sistema do tribunal

💬 Use `/help` para ver outros comandos disponíveis."""
            else:
                resposta = """⚠️ **Erro ao consultar processo**

Não foi possível acessar a API do CNJ no momento.

**Possíveis causas:**
• Número de processo inválido
• Problema na API do CNJ
• Processo não encontrado

💡 Verifique o número e tente novamente."""
            
            # Deletar mensagem de status e enviar resposta
            try:
                await status_msg.delete()
                logger.debug("✅ Mensagem de status deletada")
            except Exception as e:
                logger.warning(f"Não foi possível deletar mensagem de status: {e}")
            
            await safe_reply_text(update, resposta, use_markdown=True)
            return
            
        except Exception as e:
            logger.error(f"Erro ao consultar processo: {e}")
            context.user_data['aguardando_processo'] = False
            await safe_reply_text(update, "⚠️ Ocorreu um erro ao consultar o processo. Tente novamente.", use_markdown=False)
            return
    
    # Verificar se está aguardando nome do magistrado
    if context.user_data.get('aguardando_magistrado', False):
        try:
            from services.kermartin_service import kermartin_service
            from services.auth_service import auth_service
            
            # Verificar autenticação antes de buscar no Kermartin (com timeout)
            user_id = update.effective_user.id
            is_auth = auth_service.is_authenticated(user_id, check_timeout=True)
            
            if not is_auth:
                if auth_service.is_authenticated(user_id, check_timeout=False):
                    await safe_reply_text(
                        update,
                        "⏰ **Sessão Expirada**\n\n"
                        "Sua sessão expirou após 24 horas de inatividade.\n\n"
                        "💡 Faça login novamente com `/login` para continuar usando o Kermartin.",
                        use_markdown=True
                    )
                else:
                    await safe_reply_text(
                        update,
                        auth_service.require_auth_message(),
                        use_markdown=True
                    )
                context.user_data['aguardando_magistrado'] = False
                return
            
            # Limpar flag
            context.user_data['aguardando_magistrado'] = False
            
            # Mensagem de status
            logger.info(f"📝 Buscando magistrado: {user_message}")
            status_msg = await update.message.reply_text("🔍 *Buscando magistrado...*", parse_mode="Markdown")
            
            # Buscar magistrado
            magistrado = kermartin_service.buscar_magistrado(user_message)
            
            if magistrado:
                # Formatar resposta usando MessageFormatter
                from utils.message_formatter import message_formatter
                
                dados = magistrado.get('dados', {}) or magistrado.get('metadata', {})
                nome = dados.get('magistrado') or dados.get('nome_magistrado') or magistrado.get('nome_publico', 'N/A')
                tribunal = dados.get('tribunal') or magistrado.get('tribunal', 'N/A')
                comarca = dados.get('comarca') or magistrado.get('comarca', 'N/A')
                vara = dados.get('vara') or magistrado.get('vara', 'N/A')
                
                # Buscar estatísticas completas usando o novo método
                stats = kermartin_service.get_estatisticas_magistrado(user_message)
                
                # Usar header profissional
                resposta = message_formatter.header("PERFIL DO MAGISTRADO", message_formatter.EMOJIS['magistrado'])
                
                # Seção de identificação
                resposta += message_formatter.section("Identificação",
                    f"   👤 Nome: **{nome}**\n"
                    f"   {message_formatter.EMOJIS['tribunal']} Tribunal: {tribunal}\n"
                    f"   🏛️ Comarca: {comarca}\n"
                    f"   {message_formatter.EMOJIS['vara']} Vara: {vara}",
                    message_formatter.EMOJIS['magistrado'])
                
                resposta += f"\n{message_formatter.SEPARADOR}\n\n"
                
                # Estatísticas completas
                if stats and stats.get('total_julgados', 0) > 0:
                    resposta += message_formatter.section("Estatísticas Completas",
                        f"   {message_formatter.EMOJIS['estatistica']} Total de julgados: **{stats['total_julgados']}**\n"
                        f"   ✅ Condenações: {stats['condenacoes']} ({stats['taxa_condenacao']}%)\n"
                        f"   ❌ Absolvições: {stats['absolvicoes']} ({stats['taxa_absolvicao']}%)",
                        message_formatter.EMOJIS['estatistica'])
                    
                    # Crimes mais julgados
                    if stats.get('crimes_mais_julgados'):
                        resposta += f"\n{message_formatter.SEPARADOR}\n\n"
                        resposta += message_formatter.section("Crimes Mais Julgados",
                            "\n".join([f"   • {crime} ({count} casos)" for crime, count in stats['crimes_mais_julgados']]),
                            "📋")
                    
                    # Últimos julgados
                    if stats.get('ultimos_julgados'):
                        resposta += f"\n{message_formatter.SEPARADOR}\n\n"
                        resposta += message_formatter.section("Últimas Decisões",
                            "\n".join([
                                f"   {i+1}. Processo `{j['numero']}` - {j['decisao']} ({j.get('data', 'N/A')})"
                                for i, j in enumerate(stats['ultimos_julgados'][:5])
                            ]),
                            "📋")
                else:
                    # Estatísticas básicas se não houver dados completos
                    julgados = dados.get('julgados_consolidados', [])
                    total_julgados = len(julgados) if julgados else dados.get('total_julgados', 0)
                    
                    resposta += message_formatter.section("Estatísticas",
                        f"   {message_formatter.EMOJIS['estatistica']} Total de julgados: **{total_julgados}**",
                        message_formatter.EMOJIS['estatistica'])
                    
                    # Calcular estatísticas básicas se houver julgados
                    condenacoes = 0
                    absolvicoes = 0
                    crimes_dict = {}
                    
                    if julgados and len(julgados) > 0:
                        # Contar condenações e absolvições
                        for julgado in julgados:
                            decisao = str(julgado.get('decisao', '')).lower()
                            ementa = str(julgado.get('ementa', '')).lower()
                            
                            # Detectar tipo de decisão
                            if any(palavra in decisao for palavra in ['conden', 'pronuncia', 'absolv']):
                                if 'absolv' in decisao:
                                    absolvicoes += 1
                                elif 'conden' in decisao or 'pronuncia' in decisao:
                                    condenacoes += 1
                            elif any(palavra in ementa for palavra in ['conden', 'pronuncia']):
                                condenacoes += 1
                            elif 'absolv' in ementa:
                                absolvicoes += 1
                            
                            # Contar crimes/assuntos
                            assunto = julgado.get('assunto', '') or julgado.get('crime', '') or julgado.get('classe', '')
                            if assunto:
                                assunto_limpo = assunto.split('-')[0].strip()[:50]  # Limitar tamanho
                                crimes_dict[assunto_limpo] = crimes_dict.get(assunto_limpo, 0) + 1
                        
                        total_com_decisao = condenacoes + absolvicoes
                        
                        # Adicionar estatísticas de decisões
                        if total_com_decisao > 0:
                            taxa_condenacao = round((condenacoes / total_com_decisao) * 100, 1)
                            taxa_absolvicao = round((absolvicoes / total_com_decisao) * 100, 1)
                        
                        resposta += f"\n   • Taxa de condenação: **{taxa_condenacao}%** ({condenacoes} condenações)\n"
                        resposta += f"   • Taxa de absolvição: **{taxa_absolvicao}%** ({absolvicoes} absolvições)\n"
                    
                    # Crimes mais julgados
                    if crimes_dict:
                        crimes_ordenados = sorted(crimes_dict.items(), key=lambda x: x[1], reverse=True)[:5]
                        resposta += f"\n{message_formatter.SEPARADOR}\n\n"
                        resposta += message_formatter.section("Crimes Mais Julgados", "", "📋")
                        for crime, quantidade in crimes_ordenados:
                            porcentagem = round((quantidade / total_julgados) * 100, 1)
                            resposta += f"   • **{crime}**: {quantidade} casos ({porcentagem}%)\n"
                
                # Últimas decisões
                resposta += f"\n{message_formatter.SEPARADOR}\n\n"
                resposta += message_formatter.section("Últimas Decisões", "", "📋")
                if julgados:
                    for i, julgado in enumerate(julgados[:5], 1):
                        numero = julgado.get('numero', 'N/A')
                        data = julgado.get('data', 'N/A')
                        decisao = julgado.get('decisao', '')
                        
                        # Identificar tipo de decisão
                        tipo_decisao = ""
                        if decisao:
                            decisao_lower = decisao.lower()
                            if 'conden' in decisao_lower or 'pronuncia' in decisao_lower:
                                tipo_decisao = "🔴 Condenação"
                            elif 'absolv' in decisao_lower:
                                tipo_decisao = "🟢 Absolvição"
                            else:
                                tipo_decisao = "⚖️ Decisão"
                        
                        resposta += f"\n   **{i}.** `{numero}`\n"
                        if tipo_decisao:
                            resposta += f"      {tipo_decisao}\n"
                        resposta += f"      {message_formatter.EMOJIS['data']} {data}\n"
                else:
                    resposta += "\n   Nenhum julgado recente disponível.\n"
                
                # Padrão identificado (simplificado)
                if julgados and len(julgados) > 5:
                    resposta += f"\n{message_formatter.SEPARADOR}\n\n"
                    resposta += message_formatter.section("Padrão Identificado", "", message_formatter.EMOJIS['info'])
                    if condenacoes > absolvicoes * 1.5:
                        resposta += "   Magistrado tende a condenar quando há provas materiais consistentes.\n"
                    elif absolvicoes > condenacoes * 1.5:
                        resposta += "   Magistrado tende a absolver quando há dúvidas sobre as provas.\n"
                    else:
                        resposta += "   Padrão equilibrado de decisões.\n"
                
                resposta += message_formatter.footer("💡 Dados fornecidos pela base Kermartin")
            else:
                # Listar magistrados disponíveis
                magistrados = kermartin_service.listar_magistrados_disponiveis()
                if magistrados:
                    resposta = f"""⚠️ **Magistrado não encontrado**

Não encontrei um magistrado com o nome: **{user_message}**

**Magistrados disponíveis:**
"""
                    for mag in magistrados[:10]:  # Primeiros 10
                        resposta += f"• {mag}\n"
                    
                    if len(magistrados) > 10:
                        resposta += f"\n... e mais {len(magistrados) - 10} magistrados."
                    
                    resposta += "\n\n💡 Tente buscar usando parte do nome."
                else:
                    resposta = f"""⚠️ **Magistrado não encontrado**

Não encontrei um magistrado com o nome: **{user_message}**

A base de conhecimento ainda não possui dados deste magistrado.

💡 Tente buscar por outro nome ou use /help para mais informações."""
            
            # Deletar mensagem de status e enviar resposta
            try:
                await status_msg.delete()
                logger.debug("✅ Mensagem de status deletada")
            except Exception as e:
                logger.warning(f"Não foi possível deletar mensagem de status: {e}")
            
            await safe_reply_text(update, resposta, use_markdown=True)
            return
            
        except Exception as e:
            logger.error(f"Erro ao buscar magistrado: {e}")
            context.user_data['aguardando_magistrado'] = False
            await safe_reply_text(update, "⚠️ Ocorreu um erro ao buscar o magistrado. Tente novamente.", use_markdown=False)
            return
    
    # Verificar se está aguardando nome do promotor
    if context.user_data.get('aguardando_promotor', False):
        try:
            from services.kermartin_service import kermartin_service
            from services.auth_service import auth_service
            
            # Verificar autenticação antes de buscar no Kermartin (com timeout)
            user_id = update.effective_user.id
            is_auth = auth_service.is_authenticated(user_id, check_timeout=True)
            
            if not is_auth:
                if auth_service.is_authenticated(user_id, check_timeout=False):
                    await safe_reply_text(
                        update,
                        "⏰ **Sessão Expirada**\n\n"
                        "Sua sessão expirou após 24 horas de inatividade.\n\n"
                        "💡 Faça login novamente com `/login` para continuar usando o Kermartin.",
                        use_markdown=True
                    )
                else:
                    await safe_reply_text(
                        update,
                        auth_service.require_auth_message(),
                        use_markdown=True
                    )
                context.user_data['aguardando_promotor'] = False
                return
            
            # Limpar flag
            context.user_data['aguardando_promotor'] = False
            
            # Mensagem de status
            logger.info(f"📝 Buscando promotor: {user_message}")
            status_msg = await update.message.reply_text("🔍 *Buscando promotor...*", parse_mode="Markdown")
            
            # Buscar promotor
            promotor = kermartin_service.buscar_promotor(user_message)
            
            if promotor:
                # Formatar resposta usando MessageFormatter
                from utils.message_formatter import message_formatter
                
                nome = promotor.get('nome', 'N/A')
                comarca = promotor.get('comarca', promotor.get('dados', {}).get('comarca', 'N/A'))
                tribunal = promotor.get('tribunal', promotor.get('dados', {}).get('tribunal', 'N/A'))
                historico = promotor.get('historico', [])
                casos = promotor.get('casos', [])
                
                # Usar header profissional
                resposta = message_formatter.header("PERFIL DO PROMOTOR", message_formatter.EMOJIS['promotor'])
                
                # Seção de identificação
                resposta += message_formatter.section("Identificação",
                    f"   👤 Nome: **{nome}**\n"
                    f"   {message_formatter.EMOJIS['tribunal']} Tribunal: {tribunal}\n"
                    f"   🏛️ Comarca: {comarca}",
                    message_formatter.EMOJIS['promotor'])
                
                # Adicionar estatísticas se disponíveis
                if casos:
                    resposta += f"\n{message_formatter.SEPARADOR}\n\n"
                    resposta += message_formatter.section("Estatísticas",
                        f"   {message_formatter.EMOJIS['estatistica']} Total de casos: **{len(casos)}**",
                        message_formatter.EMOJIS['estatistica'])
                
                # Adicionar histórico recente ou casos
                if historico:
                    resposta += f"\n{message_formatter.SEPARADOR}\n\n"
                    resposta += message_formatter.section("Atuações Recentes", "", "📋")
                    for i, atuacao in enumerate(historico[:5], 1):
                        descricao = atuacao.get('descricao', 'N/A')
                        data = atuacao.get('data', 'N/A')
                        resposta += f"\n   **{i}.** {descricao}\n"
                        resposta += f"      {message_formatter.EMOJIS['data']} {data}\n"
                elif casos:
                    resposta += f"\n{message_formatter.SEPARADOR}\n\n"
                    resposta += message_formatter.section("Casos Relacionados", "", "📋")
                    for i, caso in enumerate(casos[:5], 1):
                        numero = caso.get('numero', 'N/A')
                        assunto = caso.get('assunto', 'N/A')
                        resposta += f"\n   **{i}.** `{numero}`\n"
                        resposta += f"      📋 {assunto}\n"
                else:
                    resposta += f"\n{message_formatter.SEPARADOR}\n\n"
                    resposta += "\n   Nenhuma informação adicional disponível.\n"
                
                resposta += message_formatter.footer("💡 Dados fornecidos pela base Kermartin")
            else:
                resposta = f"""⚠️ **Promotor não encontrado**

Não encontrei um promotor com o nome: **{user_message}**

A base de conhecimento ainda não possui dados deste promotor.

💡 Tente buscar por outro nome ou use /help para mais informações."""
            
            # Deletar mensagem de status e enviar resposta
            try:
                await status_msg.delete()
                logger.debug("✅ Mensagem de status deletada")
            except Exception as e:
                logger.warning(f"Não foi possível deletar mensagem de status: {e}")
            
            await safe_reply_text(update, resposta, use_markdown=True)
            return
            
        except Exception as e:
            logger.error(f"Erro ao buscar promotor: {e}")
            context.user_data['aguardando_promotor'] = False
            await safe_reply_text(update, "⚠️ Ocorreu um erro ao buscar o promotor. Tente novamente.", use_markdown=False)
            return
    
    # Verificar se está aguardando nome da comarca
    if context.user_data.get('aguardando_comarca', False):
        try:
            from services.kermartin_service import kermartin_service
            from services.auth_service import auth_service
            
            # Verificar autenticação antes de buscar no Kermartin (com timeout)
            user_id = update.effective_user.id
            is_auth = auth_service.is_authenticated(user_id, check_timeout=True)
            
            if not is_auth:
                if auth_service.is_authenticated(user_id, check_timeout=False):
                    await safe_reply_text(
                        update,
                        "⏰ **Sessão Expirada**\n\n"
                        "Sua sessão expirou após 24 horas de inatividade.\n\n"
                        "💡 Faça login novamente com `/login` para continuar usando o Kermartin.",
                        use_markdown=True
                    )
                else:
                    await safe_reply_text(
                        update,
                        auth_service.require_auth_message(),
                        use_markdown=True
                    )
                context.user_data['aguardando_comarca'] = False
                return
            
            # Limpar flag
            context.user_data['aguardando_comarca'] = False
            
            # Parse filtros da mensagem (--tipo, --status, --limite)
            # Também suporta formato alternativo: "comarca — tipo" (com em-dash)
            # Normalizar em-dash e outros separadores para padrão --filtro
            mensagem_normalizada = user_message.replace('—', ' --tipo ').replace('–', ' --tipo ')
            palavras = mensagem_normalizada.split()
            comarca_nome = []
            filtros = {'tipo': None, 'status': None, 'limite': 50}
            i = 0
            
            while i < len(palavras):
                if palavras[i].startswith('--'):
                    chave = palavras[i][2:].lower()
                    if i + 1 < len(palavras) and not palavras[i + 1].startswith('--'):
                        valor = palavras[i + 1]
                        if chave == 'limite':
                            try:
                                filtros['limite'] = int(valor)
                            except:
                                filtros['limite'] = 50
                        elif chave == 'tipo':
                            filtros['tipo'] = valor
                        elif chave == 'status':
                            filtros['status'] = valor
                        i += 2
                    else:
                        i += 1
                else:
                    comarca_nome.append(palavras[i])
                    i += 1
            
            comarca = ' '.join(comarca_nome).strip()
            
            # Normalizar acentos da comarca (a busca já faz isso, mas ajuda na exibição)
            # Não precisa fazer nada aqui, pois a busca já normaliza
            
            if not comarca:
                await safe_reply_text(
                    update,
                    "⚠️ Por favor, informe o nome da comarca.\n\n"
                    "**Exemplo:**\n"
                    "`Uberlândia`\n"
                    "`Uberlândia --tipo criminal`\n"
                    "`Uberlândia --status julgado --limite 10`",
                    use_markdown=True
                )
                return
            
            # Mensagem de status
            logger.info(f"📝 Buscando processos da comarca: {comarca} (filtros: {filtros})")
            status_msg = await update.message.reply_text("🔍 *Buscando processos da comarca...*", parse_mode="Markdown")
            
            # Buscar processos por comarca com filtros
            processos = kermartin_service.buscar_processos_por_comarca(comarca, filtros)
            
            if processos:
                # Formatar resposta usando MessageFormatter
                from utils.message_formatter import message_formatter
                
                # Usar header profissional
                resposta = message_formatter.header(f"PROCESSOS DA COMARCA: {comarca.upper()}", message_formatter.EMOJIS['tribunal'])
                
                # Mostrar filtros aplicados se houver
                filtros_texto = []
                if filtros.get('tipo'):
                    filtros_texto.append(f"Tipo: {filtros['tipo']}")
                if filtros.get('status'):
                    filtros_texto.append(f"Status: {filtros['status']}")
                if filtros_texto:
                    resposta += message_formatter.section("Filtros Aplicados",
                        "   " + " | ".join(filtros_texto),
                        "🔍")
                    resposta += f"\n{message_formatter.SEPARADOR}\n\n"
                
                # Estatísticas
                resposta += message_formatter.section("Estatísticas",
                    f"   {message_formatter.EMOJIS['estatistica']} Total encontrado: **{len(processos)}** processo(s)",
                    message_formatter.EMOJIS['estatistica'])
                
                resposta += f"\n{message_formatter.SEPARADOR}\n\n"
                
                # Lista de processos
                resposta += message_formatter.section("Processos Encontrados", "", message_formatter.EMOJIS['processo'])
                
                # Mostrar processos (limitado pelo filtro ou padrão)
                limite_exibicao = min(filtros.get('limite', 50), 20)  # Máximo 20 na exibição
                for i, processo in enumerate(processos[:limite_exibicao], 1):
                    numero = processo.get('numero', 'N/A')
                    classe = processo.get('classe', 'N/A')
                    assunto = processo.get('assunto', 'N/A')
                    status = processo.get('status', 'N/A')
                    
                    resposta += f"\n   **{i}.** `{numero}`\n"
                    resposta += f"      📋 Classe: {classe}\n"
                    assunto_limpo = str(assunto)[:50] + ('...' if len(str(assunto)) > 50 else '')
                    resposta += f"      📄 Assunto: {assunto_limpo}\n"
                    resposta += f"      {message_formatter.EMOJIS['status']} Status: {status}\n"
                
                if len(processos) > limite_exibicao:
                    resposta += f"\n   ... e mais **{len(processos) - limite_exibicao}** processo(s).\n"
                
                resposta += f"\n{message_formatter.SEPARADOR}\n\n"
                resposta += "💡 **Dicas:**\n"
                resposta += "• Use `--tipo criminal` para filtrar por tipo\n"
                resposta += "• Use `--status julgado` para filtrar por status\n"
                resposta += "• Use `--limite 10` para limitar resultados\n"
                
                resposta += message_formatter.footer("💡 Dados fornecidos pela base Kermartin")
                
                # Salvar no histórico
                try:
                    user = db_service.get_or_create_user(user_id, update.effective_user.username or "User", update.effective_user.full_name or "User")
                    if user:
                        db_service.save_chat(
                            user_id=user.id,
                            message=f"/comarca {user_message}",
                            response=f"Encontrados {len(processos)} processos em {comarca}",
                            metadata={'tipo': 'comarca', 'comarca': comarca, 'filtros': filtros, 'total': len(processos)}
                        )
                except Exception as e:
                    logger.debug(f"Erro ao salvar histórico: {e}")
            else:
                resposta = f"""⚠️ **Nenhum processo encontrado**

Não encontrei processos para a comarca: **{comarca}**

**Filtros aplicados:** {filtros if any(filtros.values()) else 'Nenhum'}

💡 **Sugestões:**
• Verifique se o nome da comarca está correto
• Tente remover os filtros: `{comarca}`
• Use `/estatisticas` para ver comarcas disponíveis"""
            
            # Deletar mensagem de status e enviar resposta
            try:
                await status_msg.delete()
                logger.debug("✅ Mensagem de status deletada")
            except Exception as e:
                logger.warning(f"Não foi possível deletar mensagem de status: {e}")
            
            await safe_reply_text(update, resposta, use_markdown=True)
            return
            
        except Exception as e:
            logger.error(f"Erro ao buscar processos por comarca: {e}")
            context.user_data['aguardando_comarca'] = False
            await safe_reply_text(update, "⚠️ Ocorreu um erro ao buscar processos da comarca. Tente novamente.", use_markdown=False)
            return
    
    # Verificar se está em modo de busca de jurisprudência
    # Verificar se está aguardando busca de jurisprudência
    if context.user_data.get('aguardando_busca', False):
        try:
            from services.jurisprudencia_service import jurisprudencia_service
            
            # Limpar flag
            context.user_data['aguardando_busca'] = False
            
            # Mensagem de status
            logger.info("📝 Enviando mensagem de status: Analisando jurisprudência...")
            status_msg = await update.message.reply_text("🔍 *Analisando sua consulta jurídica...*", parse_mode="Markdown")
            logger.debug("✅ Mensagem de status enviada")
            
            # Parse filtros da query
            query_limpa, filtros = jurisprudencia_service._parse_filtros(user_message)
            
            # Buscar jurisprudência com filtros
            resposta = await jurisprudencia_service.buscar_jurisprudencia(query_limpa, filtros)
            
            # Salvar no histórico
            try:
                user = db_service.get_or_create_user(user_id, update.effective_user.username or "User", update.effective_user.full_name or "User")
                if user:
                    db_service.save_chat(
                        user_id=user.id,
                        message=f"/buscar {user_message}",
                        response=resposta[:200] + '...' if len(resposta) > 200 else resposta,
                        metadata={'tipo': 'buscar', 'query': query_limpa, 'filtros': filtros}
                    )
            except Exception as e:
                logger.debug(f"Erro ao salvar histórico: {e}")
            
            # Deletar mensagem de status e enviar resposta
            try:
                await status_msg.delete()
                logger.debug("✅ Mensagem de status deletada")
            except Exception as e:
                logger.warning(f"Não foi possível deletar mensagem de status: {e}")
            
            # Enviar resposta com tratamento de erros
            await safe_reply_text(update, resposta, use_markdown=True)
            return
            
        except Exception as e:
            logger.error(f"Erro ao buscar jurisprudência: {e}")
            # Continuar processamento normal
    
    # Criar/buscar usuário no banco
    try:
        user = db_service.get_or_create_user(user_id, username, full_name)
    except Exception as e:
        logger.error(f"Erro ao buscar/criar usuário: {e}")
        user = None
    
    # Processar mensagem com IA
    try:
        # Mensagem de status
        logger.info("📝 Enviando mensagem de status: Processando com IA...")
        status_msg = await update.message.reply_text("🤖 *Processando com IA...*", parse_mode="Markdown")
        logger.debug("✅ Mensagem de status enviada")
        
        # Processar mensagem com tratamento de erro robusto
        try:
            logger.debug("Chamando ai_service.process_message...")
            response = await ai_service.process_message(user_message)
            logger.debug(f"Resposta recebida do AI service (tipo: {type(response)}, tamanho: {len(str(response)) if response else 0})")
        except (ValueError, SyntaxError) as e:
            error_msg = str(e).lower()
            if "incomplete escape" in error_msg or "\\x" in error_msg:
                logger.error(f"Erro de escape ao processar mensagem com IA: {e}")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                # Resposta de fallback
                response = "⚠️ Ocorreu um erro ao processar sua mensagem. Por favor, tente novamente."
            else:
                raise
        
        # Sanitizar resposta ANTES de qualquer processamento (crítico!)
        # Isso previne erros de "incomplete escape \x"
        if response:
            try:
                logger.debug("Sanitizando resposta...")
                response = sanitize_text(response)
                logger.debug("Resposta sanitizada com sucesso")
            except (ValueError, SyntaxError) as sanitize_error:
                # Se sanitização falhar, tentar sanitizar de forma mais agressiva
                error_msg = str(sanitize_error).lower()
                if "incomplete escape" in error_msg or "\\x" in error_msg:
                    logger.warning(f"Erro de escape na sanitização inicial: {sanitize_error}. Tentando sanitização agressiva...")
                    try:
                        # Tentar converter para bytes e depois de volta para string
                        response_bytes = str(response).encode('utf-8', errors='ignore')
                        response = response_bytes.decode('utf-8', errors='ignore')
                        # Remover caracteres problemáticos
                        response = ''.join(c for c in response if ord(c) >= 32 or c in ['\n', '\r', '\t'])
                        logger.debug("Sanitização agressiva concluída")
                    except Exception:
                        response = "⚠️ Ocorreu um erro ao processar a resposta. Por favor, tente novamente."
                else:
                    # Re-raise se não for erro de escape
                    raise
        
        # Salvar conversa no banco (com tratamento de erro específico para escape)
        if user:
            try:
                db_service.save_chat(
                    user_id=user.id,
                    message=user_message,
                    response=response,
                    metadata={
                        "telegram_id": user_id,
                        "username": username
                    }
                )
            except (ValueError, SyntaxError) as e:
                # Erro específico de escape ou sintaxe - logar mas não quebrar
                logger.warning(f"Erro ao salvar chat (possível problema de escape): {e}")
            except Exception:
                pass  # Ignora outros erros se DB não disponível
        
        # Deletar mensagem de status e enviar resposta
        try:
            await status_msg.delete()
            logger.debug("✅ Mensagem de status deletada")
        except Exception as e:
            logger.warning(f"Não foi possível deletar mensagem de status: {e}")
        
        # Enviar resposta com tratamento de erros
        await safe_reply_text(update, response, use_markdown=True)
        
    except (ValueError, SyntaxError) as e:
        # Erro específico de escape ou sintaxe
        error_msg = str(e)
        if "incomplete escape" in error_msg.lower() or "\\x" in error_msg.lower():
            logger.error(f"Erro de escape detectado: {e}. Aplicando correção...")
            try:
                # Tentar processar novamente com sanitização agressiva
                response = await ai_service.process_message(user_message)
                if response:
                    # Sanitização agressiva
                    response_bytes = str(response).encode('utf-8', errors='ignore')
                    response = response_bytes.decode('utf-8', errors='ignore')
                    response = ''.join(c for c in response if ord(c) >= 32 or c in ['\n', '\r', '\t'])
                    await safe_reply_text(update, response, use_markdown=False)
                    return
            except Exception:
                pass
        
        logger.error(f"Erro ao processar mensagem (escape/sintaxe): {e}")
        
        # Resposta de fallback
        fallback_response = "⚠️ Ops! Tive um problema ao processar sua mensagem.\n\n" \
                           "Por favor, tente novamente ou use os comandos disponíveis (/help)"
        
        await update.message.reply_text(fallback_response)
        
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}")
        import traceback
        logger.debug(f"Traceback completo: {traceback.format_exc()}")
        
        # Resposta de fallback
        fallback_response = "⚠️ Ops! Tive um problema ao processar sua mensagem.\n\n" \
                           "Por favor, tente novamente ou use os comandos disponíveis (/help)"
        
        await update.message.reply_text(fallback_response)

