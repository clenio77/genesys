#!/usr/bin/env python3
"""
Script para mapear estrutura completa da página de resultado do eproc
Execute após fazer uma busca real no eproc
"""

from playwright.sync_api import sync_playwright
import json
from pathlib import Path

URL_BUSCA = "https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica"

def mapear_pagina_resultado(numero_processo: str):
    """
    Faz busca real, captura página de resultado e mapeia todos os elementos
    """
    
    print(f"🗺️ Mapeando página de resultado para: {numero_processo}")
    print(f"   Isso vai abrir o navegador...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False para ver
        page = browser.new_page()
        
        try:
            # 1. Navegar e buscar
            print(f"📡 Navegando para eproc...")
            page.goto(URL_BUSCA, timeout=60000)
            
            print(f"📝 Preenchendo número do processo...")
            page.fill('#txtNumProcesso', numero_processo)
            
            print(f"🔍 Clicando em consultar...")
            page.click('#sbmNovo')
            
            # 2. Aguardar página de resultado carregar
            print(f"⏳ Aguardando resultado carregar...")
            page.wait_for_load_state('networkidle', timeout=30000)
            
            # 3. Mapear estrutura completa
            print(f"🔍 Analisando estrutura da página...")
            estrutura = page.evaluate("""
                () => {
                    const resultado = {
                        // Dados principais
                        dados_principais: {},
                        partes: [],
                        movimentacoes: [],
                        documentos: [],
                        seletores_encontrados: [],
                        todas_classes_css: []
                    };
                    
                    // Mapear dados principais
                    const buscar_texto = (seletores) => {
                        for (const sel of seletores) {
                            const el = document.querySelector(sel);
                            if (el) {
                                return {
                                    seletor: sel,
                                    texto: el.innerText.trim(),
                                    html: el.outerHTML.substring(0, 200)
                                };
                            }
                        }
                        return null;
                    };
                    
                    // Tentar encontrar número do processo
                    const numero = buscar_texto([
                        '.numero-processo', '#numeroProcesso', 
                        '.processo-numero', '[data-field="numero"]',
                        'h1', 'h2', '.titulo-processo', 
                        'div:contains("Processo")'
                    ]);
                    if (numero) {
                        resultado.dados_principais.numero = numero;
                        resultado.seletores_encontrados.push({
                            tipo: 'numero',
                            ...numero
                        });
                    }
                    
                    // Mapear todas as tabelas
                    const tabelas = document.querySelectorAll('table');
                    resultado.tabelas = [];
                    tabelas.forEach((table, idx) => {
                        const rows = table.querySelectorAll('tr');
                        const primeira_linha = rows[0] ? rows[0].innerText.toLowerCase() : '';
                        
                        const info = {
                            indice: idx,
                            seletor: `table:nth-of-type(${idx+1})`,
                            linhas: rows.length,
                            colunas: rows[0] ? rows[0].querySelectorAll('td, th').length : 0,
                            primeira_linha: primeira_linha.substring(0, 100),
                            possivel_tipo: 'desconhecido'
                        };
                        
                        // Tentar identificar tipo de tabela
                        if ('data' in primeira_linha || 'movimenta' in primeira_linha || 'historico' in primeira_linha) {
                            info.possivel_tipo = 'movimentacao';
                        } else if ('parte' in primeira_linha || 'autor' in primeira_linha || 'reu' in primeira_linha) {
                            info.possivel_tipo = 'partes';
                        } else if ('documento' in primeira_linha || 'arquivo' in primeira_linha || 'pdf' in primeira_linha) {
                            info.possivel_tipo = 'documentos';
                        }
                        
                        resultado.tabelas.push(info);
                    });
                    
                    // Mapear links para documentos
                    const links = document.querySelectorAll('a[href]');
                    links.forEach(link => {
                        const href = link.getAttribute('href');
                        const texto = link.innerText.trim();
                        
                        if (href && (
                            href.includes('.pdf') || 
                            href.includes('documento') || 
                            href.includes('Download') ||
                            href.includes('download') ||
                            href.includes('arquivo') ||
                            href.includes('Documento')
                        )) {
                            const doc = {
                                texto: texto,
                                href: href,
                                url_completa: href.startsWith('http') ? href : (window.location.origin + (href.startsWith('/') ? href : '/' + href))
                            };
                            
                            // Classificar por tipo
                            const textoLower = texto.toLowerCase();
                            if ('senten' in textoLower) {
                                doc.tipo = 'sentenca';
                            } else if ('denunci' in textoLower) {
                                doc.tipo = 'denuncia';
                            } else if ('julgado' in textoLower || 'júri' in textoLower) {
                                doc.tipo = 'julgado';
                            } else {
                                doc.tipo = 'outro';
                            }
                            
                            resultado.documentos.push(doc);
                        }
                    });
                    
                    // Mapear todas as classes CSS únicas
                    const todas_classes = new Set();
                    document.querySelectorAll('[class]').forEach(el => {
                        el.className.split(' ').forEach(cls => {
                            if (cls && cls.length > 2 && !cls.includes('_')) {
                                todas_classes.add(cls);
                            }
                        });
                    });
                    
                    resultado.todas_classes_css = Array.from(todas_classes).slice(0, 100); // Limitar a 100
                    
                    // Mapear divs com classes interessantes
                    resultado.divs_interessantes = [];
                    document.querySelectorAll('div[class*="moviment"], div[class*="document"], div[class*="parte"], div[class*="sentenc"], div[class*="julgado"]').forEach(div => {
                        resultado.divs_interessantes.push({
                            classe: div.className,
                            texto_preview: div.innerText.trim().substring(0, 100),
                            id: div.id || null
                        });
                    });
                    
                    return resultado;
                }
            """)
            
            # 4. Salvar mapeamento
            nome_arquivo = numero_processo.replace(".", "_").replace("-", "_")
            output_dir = Path(__file__).parent
            output_dir.mkdir(exist_ok=True)
            
            arquivo_json = output_dir / f'mapeamento_resultado_{nome_arquivo}.json'
            with open(arquivo_json, 'w', encoding='utf-8') as f:
                json.dump(estrutura, f, indent=2, ensure_ascii=False)
            
            # 5. Capturar HTML completo
            html = page.content()
            arquivo_html = output_dir / f'html_resultado_{nome_arquivo}.html'
            with open(arquivo_html, 'w', encoding='utf-8') as f:
                f.write(html)
            
            # 6. Screenshot
            arquivo_screenshot = output_dir / f'screenshot_resultado_{nome_arquivo}.png'
            page.screenshot(path=str(arquivo_screenshot), full_page=True)
            
            print(f"\n✅ Mapeamento concluído!")
            print(f"   📄 JSON: {arquivo_json}")
            print(f"   📄 HTML: {arquivo_html}")
            print(f"   📸 Screenshot: {arquivo_screenshot}")
            print(f"\n📊 Resumo:")
            print(f"   • Tabelas encontradas: {len(estrutura.get('tabelas', []))}")
            print(f"   • Documentos encontrados: {len(estrutura.get('documentos', []))}")
            print(f"   • Classes CSS: {len(estrutura.get('todas_classes_css', []))}")
            print(f"   • Divs interessantes: {len(estrutura.get('divs_interessantes', []))}")
            
            return estrutura
            
        except Exception as e:
            print(f"❌ Erro durante mapeamento: {e}")
            import traceback
            traceback.print_exc()
        finally:
            input("\nPressione Enter para fechar o navegador...")
            browser.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        numero_teste = sys.argv[1]
    else:
        numero_teste = "0878961-59.2013.8.13.0702"
        print(f"⚠️ Usando processo padrão: {numero_teste}")
        print(f"   Para usar outro: python mapear_resultado_eproc.py <numero_processo>")
        print()
    
    mapear_pagina_resultado(numero_teste)

