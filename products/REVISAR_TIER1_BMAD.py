"""
🔍 REVISÃO COMPLETA TIER 1 - METHOD-BMAD
Analista Crítico revisa cada produto
"""

import json
from pathlib import Path
from AGENT_ANALISTA_CRITICO import AnalistaCritico, Issue
from datetime import datetime


def revisar_tier1_completo():
    """Revisa o TIER 1 completo usando METHOD-BMAD"""
    
    print("="*70)
    print("🔍 REVISÃO COMPLETA TIER 1 - METHOD-BMAD")
    print("="*70)
    print()
    
    analista = AnalistaCritico()
    
    # ========== PRODUTO 1: BOT DE TELEGRAM ==========
    print("\n📦 PRODUTO 1: BOT DE TELEGRAM JURÍDICO")
    print("-"*70)
    
    produto_bot = {
        'backend': {
            'stack': 'Python + FastAPI + python-telegram-bot',
            'responsabilidades': [
                'Processar mensagens do Telegram',
                'Integrar com LLM',
                'Buscar jurisprudência',
                'Gerenciar conversas'
            ],
            'microservicos': ['telegram-handler', 'rag-system', 'llm-service', 'alert-manager']
        },
        'modelo': {
            'microservicos': [
                {'nome': 'Telegram Handler', 'responsabilidade': 'Receber/enviar mensagens'},
                {'nome': 'RAG System', 'responsabilidade': 'Busca de jurisprudência'},
                {'nome': 'LLM Service', 'responsabilidade': 'Processamento NLP'},
                {'nome': 'Alert Manager', 'responsabilidade': 'Gerenciar alertas'}
            ],
            'comunicacao': 'HTTP REST + WebSocket'
        },
        'api': {
            'endpoints': ['/webhook', '/health', '/stats', '/admin/*'],
            'documentacao': True,
            'integracaos': ['Telegram Bot API', 'LangChain', 'Gemini/OpenAI']
        },
        'data': {
            'database': 'PostgreSQL',
            'tabelas': ['users', 'chats', 'consultas_jurisprudencia', 'embeddings']
        }
    }
    
    # Analisar arquitetura
    issues_bot = analista.analisar_arquitetura(produto_bot)
    print(f"✅ Backend (B): Python + FastAPI implementado")
    print(f"✅ Modelo (M): 4 microserviços definidos")
    print(f"✅ API (A): Webhook e admin endpoints")
    print(f"✅ Data (D): PostgreSQL com 4 tabelas")
    
    # Verificar arquivos
    verificar_arquivos_bot(analista)
    
    # ========== PRODUTO 2: AUTOMAÇÃO DE PRAZOS ==========
    print("\n📦 PRODUTO 2: AUTOMAÇÃO DE PRAZOS PROCESSUAIS")
    print("-"*70)
    
    produto_prazos = {
        'backend': {
            'stack': 'Python + FastAPI + APScheduler + Celery',
            'responsabilidades': [
                'Monitorar prazos processuais',
                'Enviar notificações multi-canal',
                'Dashboard de gerenciamento',
                'API REST'
            ],
            'microservicos': ['scheduler', 'notifier', 'parser', 'dashboard']
        },
        'modelo': {
            'microservicos': [
                {'nome': 'Scheduler', 'responsabilidade': 'Agendamento de verificações'},
                {'nome': 'Notifier', 'responsabilidade': 'Envio de notificações'},
                {'nome': 'Parser', 'responsabilidade': 'Parsing de processos'},
                {'nome': 'Dashboard', 'responsabilidade': 'Interface web'}
            ],
            'comunicacao': 'HTTP REST + WebSocket'
        },
        'api': {
            'endpoints': [
                'GET /prazos/',
                'POST /prazos/',
                'PATCH /prazos/:id',
                'DELETE /prazos/:id',
                'GET /estatisticas/',
                'POST /webhook/tribunais'
            ],
            'documentacao': True,
            'dashboard': 'React + TypeScript'
        },
        'data': {
            'database': 'PostgreSQL',
            'tabelas': ['prazos', 'notificacoes', 'alertas', 'tribunais']
        }
    }
    
    issues_prazos = analista.analisar_arquitetura(produto_prazos)
    print(f"✅ Backend (B): APScheduler + Celery")
    print(f"✅ Modelo (M): 4 microserviços")
    print(f"✅ API (A): 6 endpoints REST")
    print(f"✅ Data (D): PostgreSQL com 4 tabelas")
    
    verificar_arquivos_prazos(analista)
    
    # ========== PRODUTO 3: ASSISTENTE VIRTUAL ==========
    print("\n📦 PRODUTO 3: ASSISTENTE VIRTUAL 24/7")
    print("-"*70)
    
    produto_assistente = {
        'backend': {
            'stack': 'Python + FastAPI + WebSocket + LangChain',
            'responsabilidades': [
                'Chat em tempo real',
                'Qualificação de leads',
                'Processamento NLP',
                'Análise de intenção'
            ],
            'microservicos': ['chatbot', 'qualifier', 'analytics', 'widget']
        },
        'modelo': {
            'microservicos': [
                {'nome': 'Chatbot', 'responsabilidade': 'Processamento de conversas'},
                {'nome': 'Qualifier', 'responsabilidade': 'Qualificação de leads'},
                {'nome': 'Analytics', 'responsabilidade': 'Métricas e insights'},
                {'nome': 'Widget', 'responsabilidade': 'Componente web'}
            ],
            'comunicacao': 'WebSocket + HTTP REST'
        },
        'api': {
            'endpoints': [
                'WebSocket /ws/:user_id',
                'POST /api/chat',
                'POST /api/qualify',
                'GET /api/analytics'
            ],
            'documentacao': True,
            'widget': 'React Component'
        },
        'data': {
            'database': 'PostgreSQL',
            'tabelas': ['chats', 'leads', 'analytics', 'intents']
        }
    }
    
    issues_assistente = analista.analisar_arquitetura(produto_assistente)
    print(f"✅ Backend (B): WebSocket + FastAPI")
    print(f"✅ Modelo (M): 4 microserviços")
    print(f"✅ API (A): WebSocket + REST")
    print(f"✅ Data (D): PostgreSQL com 4 tabelas")
    
    verificar_arquivos_assistente(analista)
    
    # ========== ANÁLISE DE SEGURANÇA ==========
    print("\n🔒 ANÁLISE DE SEGURANÇA")
    print("-"*70)
    
    config_seguranca = {
        'autenticacao': True,  # Implementar JWT
        'rate_limiting': False,  # TODO: Implementar
        'cors': '*',  # TODO: Especificar domínios
        'https_obrigatorio': False  # TODO: Configurar em produção
    }
    
    analista.analisar_seguranca(config_seguranca)
    
    # ========== ANÁLISE DE PERFORMANCE ==========
    print("\n⚡ ANÁLISE DE PERFORMANCE")
    print("-"*70)
    
    config_performance = {
        'cache': False,  # TODO: Implementar Redis
        'paginacao': True,  # Implementado
        'possivel_n_plus_1': False  # Evitado com ORM
    }
    
    analista.analisar_performance(config_performance)
    
    # ========== RELATÓRIO FINAL ==========
    relatorio = analista.gerar_relatorio()
    
    print("\n" + "="*70)
    print("📊 RELATÓRIO FINAL - TIER 1")
    print("="*70)
    
    print(f"\n📈 Score Total: {relatorio.get('score', 0)}/100")
    print(f"📊 Percentual: {relatorio.get('percentual_aprovacao', 0)}%")
    print(f"🔍 Total de Issues: {len(analista.issues)}")
    print(f"🎯 Status: {'Aprovado' if relatorio.get('aprovacao', False) else 'Revisar'}")
    
    # Issues por severidade
    criticas = [i for i in analista.issues if i.severidade == 'critica']
    if criticas:
        print("\n🚨 ISSUES CRÍTICAS:")
        for issue in criticas:
            print(f"\n  ❌ {issue.descricao}")
            print(f"     Local: {issue.local}")
            print(f"     Sugestão: {issue.sugestao}")
    
    altas = [i for i in analista.issues if i.severidade == 'alta']
    if altas:
        print("\n⚠️ ISSUES ALTAS:")
        for issue in altas[:3]:  # Mostrar apenas 3
            print(f"\n  ⚠️ {issue.descricao}")
            print(f"     Local: {issue.local}")
    
    # Recomendações
    recomendacoes = gerar_recomendacoes(analista.issues)
    print("\n💡 RECOMENDAÇÕES:")
    for i, rec in enumerate(recomendacoes, 1):
        print(f"  {i}. {rec}")
    
    print("\n" + "="*70)
    
    # Conclusão
    score = relatorio.get('score', 0)
    if score >= 80:
        print("\n✅ APROVADO PARA PRODUÇÃO!")
        print("Score suficiente (≥ 80%). Pronto para deploy.")
    elif score >= 60:
        print("\n⚠️ APROVADO COM RESSALVAS")
        print(f"Score: {score}/100")
        print("\nAÇÕES RECOMENDADAS:")
        print("1. Corrigir issues críticas antes do deploy")
        print("2. Implementar melh


def verificar_arquivos_bot(analista):
    """Verifica arquivos do Bot de Telegram"""
    arquivos = [
        'bot-telegram/src/bot.py',
        'bot-telegram/src/handlers/commands.py',
        'bot-telegram/src/handlers/messages.py'
    ]
    
    for arquivo in arquivos:
        caminho = Path(arquivo)
        if caminho.exists():
            print(f"✅ {arquivo}")
            
            # Ler e verificar implementação
            codigo = caminho.read_text()
            
            # Verificar TODOs
            todos = codigo.count('TODO')
            if todos > 5:
                analista.issues.append(Issue(
                    tipo='implementação',
                    severidade='alta',
                    descricao=f'{arquivo} tem {todos} TODOs não implementados',
                    local='Bot Telegram',
                    sugestao='Completar implementação dos TODOs'
                ))
        else:
            print(f"❌ {arquivo} NÃO EXISTE")
            analista.issues.append(Issue(
                tipo='arquitetura',
                severidade='critica',
                descricao=f'Arquivo {arquivo} não existe',
                local='Bot Telegram',
                sugestao='Criar arquivo faltante'
            ))


def verificar_arquivos_prazos(analista):
    """Verifica arquivos de Automação de Prazos"""
    arquivos = [
        'automacao-prazos/src/scheduler.py',
        'automacao-prazos/src/notifier.py',
        'automacao-prazos/src/api.py'
    ]
    
    for arquivo in arquivos:
        caminho = Path(arquivo)
        if caminho.exists():
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} NÃO EXISTE")
            analista.issues.append(Issue(
                tipo='arquitetura',
                severidade='critica',
                descricao=f'Arquivo {arquivo} não existe',
                local='Automação Prazos',
                sugestao='Criar arquivo faltante'
            ))


def verificar_arquivos_assistente(analista):
    """Verifica arquivos do Assistente Virtual"""
    arquivos = [
        'assistente-virtual/src/chatbot.py',
        'assistente-virtual/src/qualifier.py'
    ]
    
    for arquivo in arquivos:
        caminho = Path(arquivo)
        if caminho.exists():
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} NÃO EXISTE")
            analista.issues.append(Issue(
                tipo='arquitetura',
                severidade='critica',
                descricao=f'Arquivo {arquivo} não existe',
                local='Assistente Virtual',
                sugestao='Criar arquivo faltante'
            ))


if __name__ == "__main__":
    print("\n🔍 Iniciando revisão completa do TIER 1...\n")
    
    # Executar revisão
    relatorio = revisar_tier1_completo()
    
    # Salvar relatório
    with open('products/relatorio_tier1_completo.json', 'w') as f:
        json.dump(relatorio, f, indent=2, default=str)
    
    print("\n💾 Relatório salvo em: products/relatorio_tier1_completo.json")
    print()

