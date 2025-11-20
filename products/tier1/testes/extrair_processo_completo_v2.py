#!/usr/bin/env python3
"""
Script V2 - Extração com melhor debug e análise da página
"""

from playwright.sync_api import sync_playwright
import json
from datetime import datetime
from pathlib import Path

URL_BUSCA = "https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica"

def extrair_processo_completo_v2(numero_processo: str, debug: bool = True):
    """
    Versão melhorada com debug e análise de estrutura
    """
    
    print(f"🔍 Extraindo processo: {numero_processo}")
    print(f"   Modo debug: {'ATIVADO' if debug else 'DESATIVADO'}")
    
    dados_completos = {
        'numero': numero_processo,
        'data_extracao': datetime.now().isoformat(),
        'fonte': 'eproc_tjmg',
        'debug': {},
        'dados_principais': {},
        'partes': [],
        'movimentacoes': [],
        'sentencas': [],
        'julgados': [],
        'denuncias': [],
        'documentos': []
    }
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not debug)  # Mostrar navegador se debug
        page = browser.new_page()
        
        try:
            # Buscar processo
            print(f"\n📡 1. Acessando formulário de busca...")
            page.goto(URL_BUSCA, timeout=60000)
            
            # Verificar se está na página correta
            titulo_pagina = page.title()
            print(f"   Título da página: {titulo_pagina}")
            
            print(f"📝 2. Preenchendo número do processo...")
            page.fill('#txtNumProcesso', numero_processo)
            
            print(f"🔍 3. Clicando em consultar...")
            page.click('#sbmNovo')
            
            print(f"⏳ 4. Aguardando resultado...")
            try:
                # Aguardar mudança de URL ou conteúdo
                page.wait_for_load_state('networkidle', timeout=30000)
                
                # Verificar se mudou de página
                nova_url = page.url
                novo_titulo = page.title()
                print(f"   URL após busca: {nova_url}")
                print(f"   Título após busca: {novo_titulo}")
                
                # Aguardar um pouco mais para conteúdo carregar
                page.wait_for_timeout(3000)
                
            except Exception as e:
                print(f"   ⚠️ Erro ao aguardar: {e}")
            
            # CAPTURAR HTML COMPLETO PARA ANÁLISE
            print(f"\n📸 5. Capturando estrutura da página...")
            html_completo = page.content()
            
            # Salvar HTML para análise
            nome_arquivo = numero_processo.replace(".", "_").replace("-", "_")
            output_dir = Path(__file__).parent
            output_dir.mkdir(exist_ok=True)
            
            arquivo_html = output_dir / f'html_debug_{nome_arquivo}.html'
            with open(arquivo_html, 'w', encoding='utf-8') as f:
                f.write(html_completo)
            print(f"   ✅ HTML salvo: {arquivo_html}")
            
            # Screenshot
            arquivo_screenshot = output_dir / f'screenshot_debug_{nome_arquivo}.png'
            page.screenshot(path=str(arquivo_screenshot), full_page=True)
            print(f"   ✅ Screenshot salvo: {arquivo_screenshot}")
            
            # ANÁLISE DETALHADA DA PÁGINA
            print(f"\n🔍 6. Analisando estrutura...")
            analise = page.evaluate("""
                () => {
                    const info = {
                        url: window.location.href,
                        titulo: document.title,
                        tem_formulario: !!document.querySelector('form'),
                        numero_tabelas: document.querySelectorAll('table').length,
                        numero_links: document.querySelectorAll('a[href]').length,
                        numero_divs: document.querySelectorAll('div').length,
                        todas_classes: [],
                        tabelas_info: [],
                        links_importantes: [],
                        textos_principais: []
                    };
                    
                    // Coletar todas as classes CSS
                    document.querySelectorAll('[class]').forEach(el => {
                        el.className.split(' ').forEach(cls => {
                            if (cls && cls.length > 2 && !info.todas_classes.includes(cls)) {
                                info.todas_classes.push(cls);
                            }
                        });
                    });
                    
                    // Analisar tabelas
                    document.querySelectorAll('table').forEach((table, idx) => {
                        const rows = table.querySelectorAll('tr');
                        const primeira_linha = rows[0] ? rows[0].innerText.substring(0, 200) : '';
                        const segunda_linha = rows[1] ? rows[1].innerText.substring(0, 200) : '';
                        
                        info.tabelas_info.push({
                            indice: idx,
                            linhas: rows.length,
                            colunas: rows[0] ? rows[0].querySelectorAll('td, th').length : 0,
                            primeira_linha: primeira_linha,
                            segunda_linha: segunda_linha,
                            classe: table.className || '',
                            id: table.id || ''
                        });
                    });
                    
                    // Links importantes
                    document.querySelectorAll('a[href]').forEach(link => {
                        const href = link.getAttribute('href');
                        const texto = link.innerText.trim();
                        
                        if (href && (
                            href.includes('.pdf') || 
                            href.includes('documento') || 
                            href.includes('Download') ||
                            href.includes('download') ||
                            href.includes('arquivo') ||
                            href.includes('Sentenc') ||
                            href.includes('Denunci') ||
                            href.includes('Julgado') ||
                            texto.toLowerCase().includes('senten') ||
                            texto.toLowerCase().includes('denunci') ||
                            texto.toLowerCase().includes('julgado')
                        )) {
                            info.links_importantes.push({
                                texto: texto,
                                href: href,
                                url_completa: href.startsWith('http') ? href : (window.location.origin + (href.startsWith('/') ? href : '/' + href))
                            });
                        }
                    });
                    
                    // Textos principais (h1, h2, h3, strong)
                    document.querySelectorAll('h1, h2, h3, strong, .titulo, .numero').forEach(el => {
                        const texto = el.innerText.trim();
                        if (texto && texto.length > 5 && texto.length < 100) {
                            info.textos_principais.push({
                                tag: el.tagName,
                                classe: el.className || '',
                                texto: texto
                            });
                        }
                    });
                    
                    return info;
                }
            """)
            
            dados_completos['debug'] = analise
            
            print(f"\n📊 7. Estrutura encontrada:")
            print(f"   • Tabelas: {analise['numero_tabelas']}")
            print(f"   • Links: {analise['numero_links']}")
            print(f"   • Links importantes: {len(analise['links_importantes'])}")
            print(f"   • Classes CSS únicas: {len(analise['todas_classes'])}")
            print(f"   • Textos principais: {len(analise['textos_principais'])}")
            
            # TENTAR EXTRAIR DADOS COM MÚLTIPLAS ESTRATÉGIAS
            print(f"\n🔍 8. Tentando extrair dados...")
            
            resultado = page.evaluate("""
                () => {
                    const dados = {
                        dados_principais: {},
                        partes: [],
                        movimentacoes: [],
                        sentencas: [],
                        julgados: [],
                        denuncias: [],
                        documentos: []
                    };
                    
                    // ESTRATÉGIA 1: Buscar por texto visível
                    const todo_texto = document.body.innerText;
                    
                    // Tentar encontrar número do processo no texto
                    const numero_match = todo_texto.match(/(\\d{7}-\\d{2}\\.\\d{4}\\.\\d\\.\\d{2}\\.\\d{4})/);
                    if (numero_match) {
                        dados.dados_principais.numero_encontrado = numero_match[1];
                    }
                    
                    // ESTRATÉGIA 2: Buscar em TODAS as tabelas
                    document.querySelectorAll('table').forEach((table, table_idx) => {
                        const rows = table.querySelectorAll('tr');
                        
                        rows.forEach((row, row_idx) => {
                            const cells = row.querySelectorAll('td, th');
                            const cell_texts = Array.from(cells).map(c => c.innerText.trim());
                            
                            // Se tem células com conteúdo
                            if (cell_texts.some(t => t.length > 5)) {
                                const row_data = {
                                    tabela_idx: table_idx,
                                    linha_idx: row_idx,
                                    colunas: cell_texts,
                                    texto_completo: row.innerText.trim()
                                };
                                
                                // Tentar identificar tipo
                                const texto_lower = row.innerText.toLowerCase();
                                
                                if (texto_lower.includes('senten')) {
                                    dados.sentencas.push(row_data);
                                }
                                if (texto_lower.includes('julgado') || texto_lower.includes('júri')) {
                                    dados.julgados.push(row_data);
                                }
                                if (texto_lower.includes('denunci')) {
                                    dados.denuncias.push(row_data);
                                }
                                if (texto_lower.includes('moviment') || texto_lower.includes('historico')) {
                                    dados.movimentacoes.push(row_data);
                                }
                                if (texto_lower.includes('parte') || texto_lower.includes('autor') || texto_lower.includes('reu')) {
                                    dados.partes.push(row_data);
                                }
                            }
                        });
                    });
                    
                    // ESTRATÉGIA 3: Buscar TODOS os links
                    document.querySelectorAll('a[href]').forEach(link => {
                        const href = link.getAttribute('href');
                        const texto = link.innerText.trim().replace(/\\s+/g, ' ');
                        
                        if (href) {
                            const url_completa = href.startsWith('http') ? href : 
                                                (window.location.origin + (href.startsWith('/') ? href : '/' + href));
                            
                            const doc = {
                                texto: texto,
                                href: href,
                                url_completa: url_completa
                            };
                            
                            const textoLower = texto.toLowerCase();
                            if (textoLower.includes('senten')) {
                                doc.tipo = 'sentenca';
                                dados.sentencas.push(doc);
                            }
                            if (textoLower.includes('denunci')) {
                                doc.tipo = 'denuncia';
                                dados.denuncias.push(doc);
                            }
                            if (textoLower.includes('julgado') || textoLower.includes('júri')) {
                                doc.tipo = 'julgado';
                                dados.julgados.push(doc);
                            }
                            
                            if (href.includes('.pdf') || textoLower.includes('pdf') || 
                                textoLower.includes('documento') || textoLower.includes('download')) {
                                dados.documentos.push(doc);
                            }
                        }
                    });
                    
                    return dados;
                }
            """)
            
            # Mesclar resultados
            dados_completos.update(resultado)
            
            # Salvar JSON
            arquivo_json = output_dir / f"processo_completo_v2_{nome_arquivo}.json"
            with open(arquivo_json, 'w', encoding='utf-8') as f:
                json.dump(dados_completos, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Extração concluída!")
            print(f"   📄 JSON: {arquivo_json}")
            print(f"\n📊 RESULTADOS:")
            print(f"   • Movimentações: {len(dados_completos['movimentacoes'])}")
            print(f"   • Sentenças: {len(dados_completos['sentencas'])}")
            print(f"   • Julgados: {len(dados_completos['julgados'])}")
            print(f"   • Denúncias: {len(dados_completos['denuncias'])}")
            print(f"   • Documentos: {len(dados_completos['documentos'])}")
            print(f"   • Partes: {len(dados_completos['partes'])}")
            
            if dados_completos['debug']['numero_tabelas'] == 0:
                print(f"\n⚠️ ATENÇÃO: Nenhuma tabela encontrada!")
                print(f"   A página pode não ter carregado corretamente.")
                print(f"   Verifique: {arquivo_html}")
            
            return dados_completos
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            if debug:
                input("\n⏸️ Pressione Enter para fechar o navegador...")
            browser.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        numero = sys.argv[1]
    else:
        numero = "0878961-59.2013.8.13.0702"
    
    # Modo debug ativado por padrão
    debug = '--no-debug' not in sys.argv
    
    resultado = extrair_processo_completo_v2(numero, debug=debug)
    
    if resultado:
        print(f"\n💡 Dica: Verifique os arquivos HTML e screenshot para análise visual")

