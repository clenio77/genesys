"""
🔍 AGENTE ARQUITETO - Análise do TIER 1
Analisa se a implementação está completa
"""

import json
from pathlib import Path
from AGENT_ANALISTA_CRITICO import AnalistaCritico, Issue


def analisar_tier1():
    """Analisa a implementação do TIER 1"""
    
    print("🏗️ AGENTE ARQUITETO: Analisando TIER 1...\n")
    
    analista = AnalistaCritico()
    
    # Analisar estrutura de arquivos
    tier1_path = Path(".")
    issues_arquivos = verificar_arquivos_essenciais(tier1_path)
    
    # Adicionar issues encontrados
    for issue in issues_arquivos:
        analista.issues.append(issue)
    
    # Analisar cada produto
    print("\n📦 Analisando produtos...")
    
    produtos = {
        'Bot de Telegram': {
            'pasta': 'bot-telegram',
            'arquivos_essenciais': ['bot.py', 'handlers/commands.py', 'handlers/messages.py']
        },
        'Automação de Prazos': {
            'pasta': 'automacao-prazos',
            'arquivos_essenciais': ['scheduler.py', 'notifier.py', 'api.py']
        },
        'Assistente Virtual': {
            'pasta': 'assistente-virtual',
            'arquivos_essenciais': ['chatbot.py', 'qualifier.py']
        }
    }
    
    for nome, info in produtos.items():
        print(f"\n✓ {nome}:")
        
        pasta = tier1_path / info['pasta'] / 'src'
        
        for arquivo in info['arquivos_essenciais']:
            caminho = pasta / arquivo
            
            if caminho.exists():
                print(f"  ✅ {arquivo}")
                
                # Ler e analisar código
                codigo = caminho.read_text()
                
                # Verificar se tem implementação (não só TODO)
                if 'TODO' in codigo:
                    # Analisar quantos TODOs
                    todos_count = codigo.count('TODO')
                    if todos_count > 3:
                        analista.issues.append(Issue(
                            tipo='implementação',
                            severidade='alta',
                            descricao=f'{arquivo} tem {todos_count} TODOs não implementados',
                            local=nome,
                            sugestao='Completar implementação removendo TODOs'
                        ))
            else:
                print(f"  ❌ {arquivo} NÃO EXISTE")
                analista.issues.append(Issue(
                    tipo='arquitetura',
                    severidade='critica',
                    descricao=f'Arquivo {arquivo} não existe no {nome}',
                    local=nome,
                    sugestao='Criar arquivo faltante'
                ))
    
    # Verificar arquivos compartilhados
    print("\n🔗 Verificando código compartilhado...")
    shared_path = Path('shared')
    
    arquivos_compartilhados = [
        'config/settings.py',
        'config/database.py',
        'database/models.py',
        'utils/logger.py',
        'utils/helpers.py'
    ]
    
    for arquivo in arquivos_compartilhados:
        caminho = shared_path / arquivo
        if caminho.exists():
            print(f"  ✅ {arquivo}")
        else:
            print(f"  ❌ {arquivo} NÃO EXISTE")
            analista.issues.append(Issue(
                tipo='arquitetura',
                severidade='critica',
                descricao=f'Arquivo compartilhado {arquivo} não existe',
                local='shared',
                sugestao='Criar arquivo compartilhado faltante'
            ))
    
    # Gerar relatório
    relatorio = analista.gerar_relatorio()
    
    print("\n" + "="*60)
    print("📊 RELATÓRIO FINAL")
    print("="*60)
    print(f"\nScore: {relatorio['score']}/100")
    print(f"Percentual: {relatorio['percentual_aprovacao']}%")
    print(f"Total de Issues: {relatorio['total_issues']}")
    print(f"Status: {relatorio['message']}")
    
    # Issues críticas
    if relatorio['issues_criticas']:
        print("\n🚨 ISSUES CRÍTICAS:")
        for issue in relatorio['issues_criticas']:
            print(f"  - {issue['descricao']}")
            print(f"    Local: {issue['local']}")
            print(f"    Sugestão: {issue['sugestao']}\n")
    
    # Recomendações
    print("\n💡 RECOMENDAÇÕES:")
    for rec in relatorio['recomendacoes']:
        print(f"  - {rec}")
    
    print("\n" + "="*60)
    
    # Conclusão
    if relatorio.get('aprovacao', False):
        print("✅ TIER 1 ESTÁ COMPLETO!")
        print("Próximo passo: Passar para AGENTE QA")
    else:
        print("⚠️ TIER 1 PRECISA DE AJUSTES")
        print("Próximo passo: Chamar AGENTE DEV para completar")
    
    return relatorio


def verificar_arquivos_essenciais(tier1_path):
    """Verifica se arquivos essenciais existem"""
    issues = []
    
    arquivos_essenciais = [
        'docker-compose.yml',
        'requirements.txt',
        'README.md',
        'env.example',
        'shared/config/settings.py',
        'shared/config/database.py',
        'shared/database/models.py'
    ]
    
    for arquivo in arquivos_essenciais:
        caminho = tier1_path / arquivo
        if not caminho.exists():
            issues.append(Issue(
                tipo='arquitetura',
                severidade='critica',
                descricao=f'Arquivo essencial {arquivo} não existe',
                local='tier1',
                sugestao=f'Criar arquivo {arquivo}'
            ))
    
    return issues


if __name__ == "__main__":
    relatorio = analisar_tier1()
    
    # Salvar relatório
    with open('products/relatorio_analise_tier1.json', 'w') as f:
        json.dump(relatorio, f, indent=2, default=str)
    
    print("\n💾 Relatório salvo em: products/relatorio_analise_tier1.json")

