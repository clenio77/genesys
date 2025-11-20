"""
Testes para o Agente Analista Crítico
"""

from AGENT_ANALISTA_CRITICO import AnalistaCritico, Issue
import json


def test_analista_aprova_codigo_bom():
    """Testa análise de código bem estruturado"""
    analista = AnalistaCritico()
    
    produto = {
        'backend': {
            'stack': 'Python + FastAPI',
            'responsabilidades': ['processar mensagens'],
            'microservicos': ['handler']
        },
        'modelo': {
            'microservicos': ['handler'],
            'comunicacao': 'HTTP'
        },
        'api': {
            'endpoints': ['/webhook', '/health'],
            'documentacao': True
        },
        'data': {
            'database': 'PostgreSQL',
            'tabelas': ['users', 'chats']
        }
    }
    
    analista.analisar_arquitetura(produto)
    analista.analisar_seguranca({
        'autenticacao': True,
        'rate_limiting': True,
        'cors': 'https://genesys.com.br',
        'https_obrigatorio': True
    })
    analista.analisar_performance({
        'cache': True,
        'paginacao': True,
        'possivel_n_plus_1': False
    })
    
    relatorio = analista.gerar_relatorio()
    
    assert relatorio['score'] >= 80, "Score baixo para código bom"
    assert relatorio['aprovacao'] == True, "Deve ser aprovado"
    
    print("✅ Teste de aprovação passou!")
    print(f"Score: {relatorio['score']}/100")
    print(f"Status: {relatorio['message']}")


def test_analista_reprova_codigo_ruim():
    """Testa análise de código mal estruturado"""
    analista = AnalistaCritico()
    
    produto = {
        'backend': {},
        'modelo': {},
        'api': {},
        'data': {}
    }
    
    analista.analisar_arquitetura(produto)
    analista.analisar_seguranca({
        'autenticacao': False,
        'rate_limiting': False,
        'cors': '*',
        'https_obrigatorio': False
    })
    
    # Adicionar código problemático
    codigo_ruim = """
    import *
    eval(user_input)
    query = "SELECT * FROM users WHERE id = " + user_id
    """
    analista.analisar_codigo(codigo_ruim)
    
    relatorio = analista.gerar_relatorio()
    
    assert len(relatorio['issues_criticas']) > 0, "Deve encontrar issues críticas"
    assert relatorio['score'] < 60, "Score deve ser baixo"
    
    print("✅ Teste de reprovação passou!")
    print(f"Score: {relatorio['score']}/100")
    print(f"Issues críticas: {len(relatorio['issues_criticas'])}")
    print(f"Status: {relatorio['message']}")


def test_analista_gera_recomendacoes():
    """Testa geração de recomendações"""
    analista = AnalistaCritico()
    
    # Produto com issues
    produto = {
        'backend': {'stack': 'Python'},
        'modelo': {},
        'api': {'endpoints': []},
        'data': {}
    }
    
    analista.analisar_arquitetura(produto)
    relatorio = analista.gerar_relatorio()
    
    assert len(relatorio['recomendacoes']) > 0, "Deve gerar recomendações"
    
    print("✅ Teste de recomendações passou!")
    print("\nRecomendações:")
    for rec in relatorio['recomendacoes']:
        print(f"  - {rec}")


if __name__ == "__main__":
    print("🧪 Testando Agente Analista Crítico...\n")
    
    test_analista_aprova_codigo_bom()
    print()
    
    test_analista_reprova_codigo_ruim()
    print()
    
    test_analista_gera_recomendacoes()
    
    print("\n✅ Todos os testes passaram!")

