#!/usr/bin/env python3
"""
Script de debug para entender por que a extração não está funcionando
"""

from playwright.sync_api import sync_playwright
import json
from pathlib import Path

URL_BUSCA = "https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica"

def debug_extracao(numero_processo: str):
    """
    Faz busca e analisa detalhadamente o que aparece na página
    """
    
    print(f"🔍 DEBUG - Processo: {numero_processo}")
    print("=" * 60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Mostrar navegador
        page = browser.new_page()
        
        try:
            # 1. Acessar formulário
            print(f"\n📡 1. Acessando formulário de busca...")
            page.goto(URL_BUSCA, timeout=60000)
            print(f"   ✅ Página carregada")
            
            # 2. Preencher e buscar
            print(f"\n📝 2. Preenchendo formulário...")
            page.fill('#txtNumProcesso', numero_processo)
            print(f"   ✅ Número preenchido: {numero_processo}")
            
            print(f"\n🔍 3. Clicando em consultar...")
            page.click('#sbmNovo')
            
            # 3. Aguardar com múltiplas estratégias
            print(f"\n⏳ 4. Aguardando resultado...")
            
            # Aguardar mudança de URL
            try:
                page.wait_for_url('**/externo_controlador.php**', timeout=15000)
                print(f"   ✅ URL mudou (página de resultado)")
            except:
                print(f"   ⚠️ URL não mudou, mas continuando...")
            
            # Aguardar carregamento
            page.wait_for_load_state('networkidle', timeout=30000)
            page.wait_for_timeout(5000)  # Aguardar mais tempo
            
            # Verificar URL e título
            url_atual = page.url
            titulo_atual = page.title()
            print(f"\n📊 5. Estado atual:")
            print(f"   URL: {url_atual}")
            print(f"   Título: {titulo_atual}")
            
            # 4. Análise completa da página
            print(f"\n🔍 6. Analisando conteúdo da página...")
            analise_completa = page.evaluate(f"""
                () => {{
                    const numero_processo = '{numero_processo}';
                    
                    const info = {{
                        url: window.location.href,
                        titulo: document.title,
                        url_contem_processo: window.location.href.includes('processo'),
                        url_contem_consulta: window.location.href.includes('consulta'),
                        textos_visiveis: [],
                        tabelas_encontradas: [],
                        links_encontrados: [],
                        formularios_encontrados: [],
                        mensagens_erro: [],
                        elementos_interessantes: []
                    }};
                    
                    // Coletar todos os textos visíveis importantes
                    const elementos_texto = document.querySelectorAll('h1, h2, h3, h4, .titulo, .numero, strong, b, .destaque');
                    elementos_texto.forEach(el => {{
                        const texto = el.innerText.trim();
                        if (texto && texto.length > 3 && texto.length < 200) {{
                            info.textos_visiveis.push({{
                                tag: el.tagName,
                                classe: el.className || '',
                                id: el.id || '',
                                texto: texto
                            }});
                        }}
                    }});
                    
                    // Analisar TODAS as tabelas
                    document.querySelectorAll('table').forEach((table, idx) => {{
                        const rows = table.querySelectorAll('tr');
                        const primeira_linha = rows[0] ? rows[0].innerText.trim().substring(0, 300) : '';
                        const primeira_coluna = rows[0] ? rows[0].querySelectorAll('td, th')[0]?.innerText.trim() : '';
                        
                        info.tabelas_encontradas.push({{
                            indice: idx,
                            linhas: rows.length,
                            colunas: rows[0] ? rows[0].querySelectorAll('td, th').length : 0,
                            primeira_linha_completa: primeira_linha,
                            primeira_coluna: primeira_coluna,
                            classe: table.className || '',
                            id: table.id || '',
                            linhas_preview: Array.from(rows).slice(0, 3).map(r => r.innerText.trim().substring(0, 200))
                        }});
                    }});
                    
                    // Analisar TODOS os links
                    document.querySelectorAll('a[href]').forEach(link => {{
                        const href = link.getAttribute('href');
                        const texto = link.innerText.trim().replace(/\\s+/g, ' ');
                        
                        if (href && texto) {{
                            info.links_encontrados.push({{
                                texto: texto.substring(0, 100),
                                href: href,
                                url_completa: href.startsWith('http') ? href : (window.location.origin + (href.startsWith('/') ? href : '/' + href)),
                                parece_documento: href.includes('.pdf') || href.includes('documento') || texto.toLowerCase().includes('documento'),
                                parece_processo: href.includes('processo') || texto.includes(numero_processo)
                            }});
                        }}
                    }});
                    
                    // Verificar mensagens de erro ou "não encontrado"
                    const todo_texto = document.body.innerText.toLowerCase();
                    if (todo_texto.includes('não encontrado') || todo_texto.includes('nao encontrado') || 
                        todo_texto.includes('não existe') || todo_texto.includes('inexistente')) {{
                        info.mensagens_erro.push('Processo não encontrado');
                    }}
                    if (todo_texto.includes('erro') || todo_texto.includes('error')) {{
                        info.mensagens_erro.push('Mensagem de erro encontrada');
                    }}
                    
                    // Verificar se está na página de busca ainda
                    const tem_campo_busca = !!document.querySelector('#txtNumProcesso');
                    info.ainda_na_busca = tem_campo_busca;
                    
                    // Buscar elementos que podem ter dados do processo
                    const numero_no_texto = document.body.innerText.match(/(\\d{{7}}-\\d{{2}}\\.\\d{{4}}\\.\\d\\.\\d{{2}}\\.\\d{{4}})/);
                    if (numero_no_texto) {{
                        info.numero_processo_encontrado = numero_no_texto[1];
                    }}
                    
                    return info;
                }}
            """)
            
            # Salvar análise
            nome_arquivo = numero_processo.replace(".", "_").replace("-", "_")
            output_dir = Path(__file__).parent
            output_dir.mkdir(exist_ok=True)
            
            arquivo_json = output_dir / f"debug_analise_{nome_arquivo}.json"
            with open(arquivo_json, 'w', encoding='utf-8') as f:
                json.dump({
                    'numero_processo': numero_processo,
                    'analise': analise_completa
                }, f, indent=2, ensure_ascii=False)
            
            # HTML completo
            html_completo = page.content()
            arquivo_html = output_dir / f"debug_html_{nome_arquivo}.html"
            with open(arquivo_html, 'w', encoding='utf-8') as f:
                f.write(html_completo)
            
            # Screenshot
            arquivo_screenshot = output_dir / f"debug_screenshot_{nome_arquivo}.png"
            page.screenshot(path=str(arquivo_screenshot), full_page=True)
            
            print(f"\n✅ Análise salva:")
            print(f"   📄 JSON: {arquivo_json}")
            print(f"   📄 HTML: {arquivo_html}")
            print(f"   📸 Screenshot: {arquivo_screenshot}")
            
            print(f"\n📊 RESUMO DA ANÁLISE:")
            print(f"   • Ainda na página de busca: {analise_completa.get('ainda_na_busca', 'desconhecido')}")
            print(f"   • Tabelas encontradas: {len(analise_completa['tabelas_encontradas'])}")
            print(f"   • Links encontrados: {len(analise_completa['links_encontrados'])}")
            print(f"   • Textos visíveis: {len(analise_completa['textos_visiveis'])}")
            print(f"   • Mensagens de erro: {len(analise_completa['mensagens_erro'])}")
            if analise_completa.get('numero_processo_encontrado'):
                print(f"   • ✅ Número do processo encontrado no texto!")
            else:
                print(f"   • ❌ Número do processo NÃO encontrado")
            
            if analise_completa.get('mensagens_erro'):
                print(f"\n⚠️ MENSAGENS DE ERRO:")
                for msg in analise_completa['mensagens_erro']:
                    print(f"   • {msg}")
            
            if analise_completa['tabelas_encontradas']:
                print(f"\n📋 TABELAS ENCONTRADAS:")
                for i, tabela in enumerate(analise_completa['tabelas_encontradas']):
                    print(f"   Tabela {i+1}: {tabela['linhas']} linhas, {tabela['colunas']} colunas")
                    if tabela['primeira_coluna']:
                        print(f"      Primeira coluna: {tabela['primeira_coluna'][:50]}")
            
            input("\n⏸️ Pressione Enter para fechar...")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        numero = sys.argv[1]
    else:
        numero = "0878961-59.2013.8.13.0702"
    
    debug_extracao(numero)

