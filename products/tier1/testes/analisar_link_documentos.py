#!/usr/bin/env python3
"""
Script para analisar o link de documentos encontrado
"""

from playwright.sync_api import sync_playwright
import json
from pathlib import Path

def analisar_link_documentos(numero_processo: str):
    """
    Analisa o link de documentos para ver o que há disponível
    """
    
    url_docs = "https://eproc-consulta-publica-1g.tjmg.jus.br/externo_controlador.php?acao=consulta_autenticidade_documentos"
    
    print(f"🔍 Analisando link de documentos para: {numero_processo}")
    print(f"   URL: {url_docs}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Primeiro, fazer busca normal
            print(f"\n📡 1. Fazendo busca do processo...")
            page.goto("https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica")
            page.fill('#txtNumProcesso', numero_processo)
            page.click('#sbmNovo')
            page.wait_for_load_state('networkidle', timeout=30000)
            page.wait_for_timeout(2000)
            
            # Capturar URL atual
            url_apos_busca = page.url
            print(f"   URL após busca: {url_apos_busca}")
            
            # Verificar se tem link para documentos
            print(f"\n🔍 2. Procurando links de documentos...")
            links_docs = page.evaluate("""
                () => {
                    const links = [];
                    document.querySelectorAll('a[href]').forEach(link => {
                        const href = link.getAttribute('href');
                        const texto = link.innerText.trim();
                        
                        if (href && (
                            href.includes('documento') || 
                            href.includes('documentos') ||
                            href.includes('consulta_autenticidade') ||
                            texto.toLowerCase().includes('documento') ||
                            texto.toLowerCase().includes('arquivo')
                        )) {
                            links.push({
                                texto: texto,
                                href: href,
                                url_completa: href.startsWith('http') ? href : (window.location.origin + (href.startsWith('/') ? href : '/' + href))
                            });
                        }
                    });
                    return links;
                }
            """)
            
            print(f"   ✅ Encontrados {len(links_docs)} links relacionados a documentos")
            for link in links_docs:
                print(f"      • {link['texto'][:50]} → {link['url_completa']}")
            
            # Tentar acessar link de documentos
            if links_docs:
                link_principal = links_docs[0]
                print(f"\n📄 3. Acessando link de documentos...")
                print(f"   URL: {link_principal['url_completa']}")
                
                try:
                    page.goto(link_principal['url_completa'], timeout=30000)
                    page.wait_for_load_state('networkidle', timeout=30000)
                    page.wait_for_timeout(2000)
                    
                    # Analisar página de documentos
                    print(f"\n🔍 4. Analisando página de documentos...")
                    analise_docs = page.evaluate("""
                        () => {
                            const info = {
                                url: window.location.href,
                                titulo: document.title,
                                numero_tabelas: document.querySelectorAll('table').length,
                                numero_links_pdf: document.querySelectorAll('a[href*=".pdf"]').length,
                                links_pdf: [],
                                formularios: []
                            };
                            
                            // Buscar links PDF
                            document.querySelectorAll('a[href]').forEach(link => {
                                const href = link.getAttribute('href');
                                const texto = link.innerText.trim();
                                
                                if (href && (
                                    href.includes('.pdf') || 
                                    texto.toLowerCase().includes('pdf') ||
                                    texto.toLowerCase().includes('baixar') ||
                                    texto.toLowerCase().includes('download')
                                )) {
                                    info.links_pdf.push({
                                        texto: texto,
                                        href: href,
                                        url_completa: href.startsWith('http') ? href : (window.location.origin + (href.startsWith('/') ? href : '/' + href))
                                    });
                                }
                            });
                            
                            // Buscar formulários
                            document.querySelectorAll('form').forEach(form => {
                                info.formularios.push({
                                    action: form.action || '',
                                    method: form.method || '',
                                    campos: Array.from(form.querySelectorAll('input, select, textarea')).map(el => ({
                                        name: el.name || '',
                                        type: el.type || el.tagName.toLowerCase(),
                                        id: el.id || ''
                                    }))
                                });
                            });
                            
                            return info;
                        }
                    """)
                    
                    # Salvar análise
                    nome_arquivo = numero_processo.replace(".", "_").replace("-", "_")
                    output_dir = Path(__file__).parent
                    
                    arquivo_json = output_dir / f"analise_documentos_{nome_arquivo}.json"
                    with open(arquivo_json, 'w', encoding='utf-8') as f:
                        json.dump({
                            'numero_processo': numero_processo,
                            'links_encontrados': links_docs,
                            'analise_pagina_docs': analise_docs
                        }, f, indent=2, ensure_ascii=False)
                    
                    # Screenshot
                    arquivo_screenshot = output_dir / f"screenshot_documentos_{nome_arquivo}.png"
                    page.screenshot(path=str(arquivo_screenshot), full_page=True)
                    
                    # HTML
                    html_completo = page.content()
                    arquivo_html = output_dir / f"html_documentos_{nome_arquivo}.html"
                    with open(arquivo_html, 'w', encoding='utf-8') as f:
                        f.write(html_completo)
                    
                    print(f"\n✅ Análise concluída!")
                    print(f"   📄 JSON: {arquivo_json}")
                    print(f"   📸 Screenshot: {arquivo_screenshot}")
                    print(f"   📄 HTML: {arquivo_html}")
                    print(f"\n📊 Resultados:")
                    print(f"   • Links PDF encontrados: {analise_docs['numero_links_pdf']}")
                    print(f"   • Tabelas na página: {analise_docs['numero_tabelas']}")
                    print(f"   • Formulários: {len(analise_docs['formularios'])}")
                    
                except Exception as e:
                    print(f"   ❌ Erro ao acessar: {e}")
            
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
    
    analisar_link_documentos(numero)

