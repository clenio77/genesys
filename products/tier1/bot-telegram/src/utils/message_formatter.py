"""
Utilitários para formatação profissional de mensagens
Padroniza design e estilo visual do bot
"""

from typing import Dict, List, Optional, Any
from datetime import datetime


class MessageFormatter:
    """Formatador profissional de mensagens para Telegram"""
    
    # Separadores visuais refinados
    SEPARADOR = "─" * 38
    SEPARADOR_FORTE = "═" * 38
    SEPARADOR_SUBTLE = "·" * 38
    
    # Logo/Watermark sutil da Genesys (mais discreto)
    LOGO_WATERMARK = "⚡ Genesys"
    LOGO_SUBTLE = "░║╚╝╗╔═╦╩╬"  # Caracteres Unicode para efeito sutil
    
    # Emojis padronizados (expandido e mais consistente)
    EMOJIS = {
        'processo': '⚖️',
        'magistrado': '👨‍⚖️',
        'promotor': '👤',
        'prazo': '📅',
        'alerta': '🔔',
        'busca': '🔍',
        'config': '⚙️',
        'sucesso': '✅',
        'erro': '❌',
        'info': '💡',
        'estatistica': '📊',
        'cache': '💾',
        'tribunal': '🏛️',
        'vara': '⚖️',
        'data': '📅',
        'status': '📊',
        'lock': '🔒',
        'unlock': '🔓',
        'referencia': '📚',
        'jurisprudencia': '⚖️',
        'comarca': '🏛️',
        'perfil': '👤',
        'historico': '📋',
    }
    
    @classmethod
    def card(cls, titulo: str, itens: List[str], emoji: str = "📋") -> str:
        """
        Cria um card visual de informação com design refinado
        
        Args:
            titulo: Título do card
            itens: Lista de itens
            emoji: Emoji do card
            
        Returns:
            Card formatado
        """
        card = f"{emoji} **{titulo}**\n"
        for item in itens:
            card += f"   • {item}\n"
        return card
    
    @classmethod
    def section(cls, titulo: str, conteudo: str, emoji: str = "📋") -> str:
        """
        Cria uma seção formatada com melhor espaçamento
        
        Args:
            titulo: Título da seção
            conteudo: Conteúdo da seção
            emoji: Emoji da seção
            
        Returns:
            Seção formatada
        """
        return f"{emoji} **{titulo}**\n{conteudo}\n"
    
    @classmethod
    def section_compact(cls, titulo: str, conteudo: str, emoji: str = "📋") -> str:
        """
        Cria uma seção compacta (sem quebra de linha extra)
        
        Args:
            titulo: Título da seção
            conteudo: Conteúdo da seção
            emoji: Emoji da seção
            
        Returns:
            Seção formatada compacta
        """
        return f"{emoji} **{titulo}**\n{conteudo}"
    
    @classmethod
    def header(cls, titulo: str, emoji: str = "🎯") -> str:
        """
        Cria cabeçalho de mensagem com design refinado
        
        Args:
            titulo: Título principal
            emoji: Emoji do título
            
        Returns:
            Cabeçalho formatado
        """
        return f"{emoji} **{titulo}**\n{cls.SEPARADOR_FORTE}\n"
    
    @classmethod
    def footer(cls, texto: str = "💡 Dados fornecidos por Genesys Bot + Kermartin", incluir_branding: bool = True) -> str:
        """
        Cria rodapé de mensagem com watermark sutil da logo (refinado)
        
        Args:
            texto: Texto do rodapé
            incluir_branding: Se deve incluir branding da Genesys
            
        Returns:
            Rodapé formatado
        """
        footer_text = f"\n{cls.SEPARADOR}\n\n{texto}"
        
        # Branding mais sutil e elegante
        if incluir_branding:
            footer_text += f"\n\n{' ' * 22}⚡ Genesys"
        
        return footer_text
    
    @classmethod
    def watermark_subtle(cls) -> str:
        """
        Retorna apenas o watermark sutil da Genesys (sem separadores)
        Versão minimalista e discreta
        
        Returns:
            Watermark textual sutil
        """
        # Versão ultra sutil - apenas texto pequeno alinhado à direita
        return f"\n{' ' * 24}⚡ Genesys"
    
    @classmethod
    def status_badge(cls, status: str, tipo: str = "info") -> str:
        """
        Cria badge de status
        
        Args:
            status: Texto do status
            tipo: Tipo de badge (success, error, warning, info, locked)
            
        Returns:
            Badge formatado
        """
        badges = {
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "💡",
            "locked": "🔒",
            "unlocked": "🔓"
        }
        emoji = badges.get(tipo, "💡")
        return f"{emoji} {status}"
    
    @classmethod
    def formatar_processo(cls, dados: Dict[str, Any]) -> str:
        """
        Formata resposta de processo com design profissional
        
        Args:
            dados: Dados do processo
            
        Returns:
            Mensagem formatada
        """
        if "erro" in dados:
            return f"{cls.EMOJIS['erro']} **Erro na Consulta**\n\n{dados['erro']}"
        
        numero = dados.get("numero", "N/A")
        classe = dados.get("classe", "N/A")
        assunto = dados.get("assunto", "N/A")
        tribunal = dados.get("tribunal", "N/A")
        vara = dados.get("vara", "N/A")
        status = dados.get("status", "N/A")
        data_autuacao = dados.get("data_autuacao", "N/A")
        fonte = dados.get("fonte", "API CNJ")
        
        mensagem = cls.header("CONSULTA DE PROCESSO", cls.EMOJIS['processo'])
        
        mensagem += cls.section("Identificação", 
            f"   📄 Número: `{numero}`\n"
            f"   📋 Classe: {classe}\n"
            f"   📝 Assunto: {assunto}",
            cls.EMOJIS['processo'])
        
        mensagem += f"\n{cls.SEPARADOR}\n\n"
        
        mensagem += cls.section("Tribunal e Vara",
            f"   {cls.EMOJIS['tribunal']} Tribunal: {tribunal}\n"
            f"   {cls.EMOJIS['vara']} Vara: {vara}\n"
            f"   {cls.EMOJIS['status']} Status: {status}",
            cls.EMOJIS['tribunal'])
        
        mensagem += f"\n{cls.SEPARADOR}\n\n"
        
        mensagem += cls.section("Datas",
            f"   {cls.EMOJIS['data']} Autuação: {data_autuacao}",
            cls.EMOJIS['data'])
        
        # Adicionar última movimentação se disponível
        if "ultima_mov" in dados:
            mensagem += f"\n   📋 Última Movimentação:\n"
            mensagem += f"      {dados.get('ultima_mov', 'N/A')}\n"
        
        mensagem += cls.footer(f"💡 Fonte: {fonte}")
        
        return mensagem
    
    @classmethod
    def formatar_menu_principal(cls, is_authenticated: bool, ultimo_acesso: Optional[str] = None) -> str:
        """
        Formata menu principal profissional
        
        Args:
            is_authenticated: Se usuário está autenticado
            ultimo_acesso: Data do último acesso (opcional)
            
        Returns:
            Menu formatado
        """
        auth_status = cls.status_badge("Autenticado", "success") if is_authenticated else cls.status_badge("Não autenticado", "locked")
        auth_note = "✅ Acesso completo ao Kermartin" if is_authenticated else "💡 Faça /login para acesso completo"
        
        menu = cls.header("MENU PRINCIPAL - Genesys Bot", "🎯")
        
        menu += cls.section("Seu Status",
            f"   {auth_status}\n   {auth_note}",
            "👤")
        
        if ultimo_acesso:
            menu += f"\n   📅 Último acesso: {ultimo_acesso}\n"
        
        menu += f"\n{cls.SEPARADOR}\n\n"
        
        menu += cls.section("CONSULTAS",
            "   /processo - Consultar processo\n"
            "   /buscar - Buscar jurisprudência\n"
            "   /magistrado - Perfil de magistrado\n"
            f"   {'/promotor - Perfil de promotor' if is_authenticated else '/promotor - 🔒 Requer login'}\n"
            f"   {'/comarca - Processos por comarca' if is_authenticated else '/comarca - 🔒 Requer login'}",
            "📚")
        
        menu += f"\n{cls.SEPARADOR}\n\n"
        
        menu += cls.section("GESTÃO",
            "   /prazos - Seus prazos processuais\n"
            "   /alerta - Configurar alertas\n"
            "   /historico - Histórico de consultas",
            "📊")
        
        menu += f"\n{cls.SEPARADOR}\n\n"
        
        menu += cls.section("CONFIGURAÇÕES",
            "   /perfil - Meu perfil\n"
            "   /config - Configurações\n"
            "   /cache - Estatísticas de performance",
            "⚙️")
        
        menu += cls.footer("💡 Digite um comando ou faça uma pergunta em linguagem natural")
        
        return menu
    
    @classmethod
    def formatar_status_auth(cls, is_authenticated: bool, ultimo_login: Optional[str] = None, 
                           sessao_expira: Optional[str] = None) -> str:
        """
        Formata status de autenticação
        
        Args:
            is_authenticated: Se está autenticado
            ultimo_login: Data do último login
            sessao_expira: Data de expiração da sessão
            
        Returns:
            Status formatado
        """
        mensagem = cls.header("STATUS DE ACESSO", "🔐")
        
        if is_authenticated:
            mensagem += cls.status_badge("Autenticado", "success") + "\n"
            mensagem += cls.card("Benefícios",
                [
                    "Acesso completo ao Kermartin",
                    "Busca avançada disponível",
                    "Histórico de consultas ativo",
                    "Comandos premium habilitados"
                ],
                "✅")
            
            if ultimo_login:
                mensagem += f"\n📅 Último login: {ultimo_login}\n"
            if sessao_expira:
                mensagem += f"⏰ Sessão válida até: {sessao_expira}\n"
        else:
            mensagem += cls.status_badge("Não autenticado", "locked") + "\n"
            mensagem += cls.card("Limitações",
                [
                    "Acesso limitado",
                    "Apenas API CNJ disponível",
                    "Comandos premium bloqueados"
                ],
                "🔒")
            
            mensagem += "\n💡 Use /login para acesso completo\n"
        
        return mensagem
    
    @classmethod
    def formatar_resposta_ia(cls, resposta: str, pergunta: Optional[str] = None, incluir_header: bool = False) -> str:
        """
        Formata resposta da IA com design elegante
        
        Args:
            resposta: Resposta gerada pela IA
            pergunta: Pergunta original (opcional)
            incluir_header: Se deve incluir cabeçalho
            
        Returns:
            Resposta formatada
        """
        if incluir_header and pergunta:
            formatted = cls.header("RESPOSTA", "🤖")
            formatted += f"**Pergunta:** {pergunta}\n\n"
            formatted += f"{cls.SEPARADOR}\n\n"
            formatted += resposta
        else:
            formatted = resposta
        
        # Adicionar separador sutil antes do footer se não tiver
        if not formatted.endswith("\n"):
            formatted += "\n"
        
        return formatted
    
    @classmethod
    def formatar_lista_numerada(cls, itens: List[str], titulo: Optional[str] = None, emoji: str = "📋") -> str:
        """
        Formata lista numerada com design profissional
        
        Args:
            itens: Lista de itens
            titulo: Título opcional
            emoji: Emoji do título
            
        Returns:
            Lista formatada
        """
        lista = ""
        if titulo:
            lista = f"{emoji} **{titulo}**\n\n"
        
        for i, item in enumerate(itens, 1):
            lista += f"**{i}.** {item}\n"
        
        return lista
    
    @classmethod
    def formatar_info_box(cls, texto: str, tipo: str = "info") -> str:
        """
        Cria uma caixa de informação destacada
        
        Args:
            texto: Texto da informação
            tipo: Tipo (info, warning, success, error)
            
        Returns:
            Caixa formatada
        """
        emojis = {
            "info": "💡",
            "warning": "⚠️",
            "success": "✅",
            "error": "❌"
        }
        emoji = emojis.get(tipo, "💡")
        
        # Caixa com bordas sutis
        box = f"{emoji} **{tipo.upper()}**\n"
        box += f"{cls.SEPARADOR_SUBTLE}\n"
        box += f"{texto}\n"
        box += f"{cls.SEPARADOR_SUBTLE}\n"
        
        return box


# Instância global
message_formatter = MessageFormatter()

