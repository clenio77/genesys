#!/usr/bin/env python3
"""
Script para extrair TODOS os dados possíveis de um processo:
- Dados principais
- Partes
- Movimentações completas
- Sentenças
- Julgados  
- Denúncias
- Todos os documentos/arquivos
"""

from playwright.sync_api import sync_playwright
import json
from datetime import datetime
from pathlib import Path

URL_BUSCA = "https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica"

def extrair_processo_completo(numero_processo: str, salvar_arquivos: bool = True):
    """
    Extrai TODOS os dados possíveis de um processo
    """
    
    print(f"🔍 Extraindo processo completo: {numero_processo}")
    
    dados_completos = {
        'numero': numero_processo,
        'data_extracao': datetime.now().isoformat(),
        'fonte': 'eproc_tjmg',
        'dados_principais': {},
        'partes': [],
        'movimentacoes': [],
        'sentencas': [],
        'julgados': [],
        'denuncias': [],
        'documentos': [],
        'links_pdf': []
    }
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Buscar processo
            print(f"📡 Acessando eproc...")
            page.goto(URL_BUSCA, timeout=60000)
            
            print(f"📝 Preenchendo formulário...")
            page.fill('#txtNumProcesso', numero_processo)
            page.click('#sbmNovo')
            
            print(f"⏳ Aguardando resultado...")
            page.wait_for_load_state('networkidle', timeout=30000)
            page.wait_for_timeout(2000)  # Aguardar mais 2 segundos
            
            # Extrair tudo usando JavaScript
            print(f"🔍 Extraindo dados...")
            resultado = page.evaluate("""
                () => {
                    const dados = {
                        dados_principais: {},
                        partes: [],
                        movimentacoes: [],
                        sentencas: [],
                        julgados: [],
                        denuncias: [],
                        documentos: [],
                        links_pdf: []
                    };
                    
                    // Função auxiliar para buscar texto
                    const buscar_texto = (seletores) => {
                        for (const sel of seletores) {
                            try {
                                const el = document.querySelector(sel);
                                if (el && el.innerText.trim()) {
                                    return el.innerText.trim();
                                }
                            } catch(e) {}
                        }
                        return null;
                    };
                    
                    // Função auxiliar para buscar múltiplos
                    const buscar_multiplos = (seletores) => {
                        const resultados = [];
                        seletores.forEach(sel => {
                            try {
                                document.querySelectorAll(sel).forEach(el => {
                                    if (el.innerText.trim()) {
                                        resultados.push(el.innerText.trim());
                                    }
                                });
                            } catch(e) {}
                        });
                        return [...new Set(resultados)];
                    };
                    
                    // 1. DADOS PRINCIPAIS
                    dados.dados_principais = {
                        numero: buscar_texto(['.numero-processo', '#numeroProcesso', 'h1', 'h2', '.titulo-processo']),
                        classe: buscar_texto(['.classe', '.tipo-processo', 'span:contains("Classe")']),
                        vara: buscar_texto(['.vara', '.turma', '.orgao-julgador', 'span:contains("Vara")']),
                        status: buscar_texto(['.status', '.situacao', 'span:contains("Status")']),
                        comarca: buscar_texto(['.comarca', 'span:contains("Comarca")'])
                    };
                    
                    // 2. PARTES - Tentar todas as tabelas
                    const todas_tabelas = document.querySelectorAll('table');
                    todas_tabelas.forEach((table, idx) => {
                        const linhas = table.querySelectorAll('tr');
                        const primeira_linha = linhas[0] ? linhas[0].innerText.toLowerCase() : '';
                        
                        // Se parece tabela de partes
                        if (primeira_linha.includes('parte') || primeira_linha.includes('autor') || primeira_linha.includes('reu') || 
                            primeira_linha.includes('advogado') || linhas.length <= 10) {
                            
                            linhas.forEach((linha, linha_idx) => {
                                const cols = linha.querySelectorAll('td, th');
                                if (cols.length >= 2) {
                                    const texto_cols = Array.from(cols).map(c => c.innerText.trim());
                                    dados.partes.push({
                                        tipo: texto_cols[0] || '',
                                        nome: texto_cols[1] || '',
                                        completo: linha.innerText.trim(),
                                        linha_idx: linha_idx
                                    });
                                }
                            });
                        }
                    });
                    
                    // 3. MOVIMENTAÇÕES - Tentar todas as tabelas
                    todas_tabelas.forEach((table) => {
                        const linhas = table.querySelectorAll('tr');
                        const primeira_linha = linhas[0] ? linhas[0].innerText.toLowerCase() : '';
                        
                        // Se parece tabela de movimentação
                        if (primeira_linha.includes('data') || primeira_linha.includes('movimenta') || 
                            primeira_linha.includes('historico') || linhas.length > 5) {
                            
                            linhas.forEach((linha, linha_idx) => {
                                if (linha_idx === 0) return; // Pular cabeçalho
                                
                                const cols = linha.querySelectorAll('td');
                                if (cols.length >= 2) {
                                    const movimentacao = {
                                        data: cols[0]?.innerText.trim() || '',
                                        tipo: cols[1]?.innerText.trim() || '',
                                        descricao: cols.length > 2 ? cols[2]?.innerText.trim() : '',
                                        texto_completo: linha.innerText.trim(),
                                        linha_idx: linha_idx
                                    };
                                    
                                    dados.movimentacoes.push(movimentacao);
                                    
                                    // Classificar por tipo
                                    const tipoLower = movimentacao.tipo.toLowerCase();
                                    const descLower = movimentacao.descricao.toLowerCase();
                                    
                                    if (tipoLower.includes('senten') || descLower.includes('senten')) {
                                        dados.sentencas.push(movimentacao);
                                    }
                                    if (tipoLower.includes('julgado') || descLower.includes('julgado') || tipoLower.includes('júri') || descLower.includes('júri')) {
                                        dados.julgados.push(movimentacao);
                                    }
                                    if (tipoLower.includes('denunci') || descLower.includes('denunci')) {
                                        dados.denuncias.push(movimentacao);
                                    }
                                }
                            });
                        }
                    });
                    
                    // 4. DOCUMENTOS/ARQUIVOS - Todos os links
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
                            href.includes('Documento') ||
                            href.includes('.doc') ||
                            href.includes('.docx')
                        )) {
                            const url_completa = href.startsWith('http') ? href : 
                                                (window.location.origin + (href.startsWith('/') ? href : '/' + href));
                            
                            const doc = {
                                texto: texto,
                                href: href,
                                url_completa: url_completa
                            };
                            
                            // Classificar tipo de documento
                            const textoLower = texto.toLowerCase();
                            if (textoLower.includes('senten')) {
                                doc.tipo = 'sentenca';
                                dados.sentencas.push(doc);
                            } else if (textoLower.includes('denunci')) {
                                doc.tipo = 'denuncia';
                                dados.denuncias.push(doc);
                            } else if (textoLower.includes('julgado') || textoLower.includes('júri')) {
                                doc.tipo = 'julgado';
                                dados.julgados.push(doc);
                            } else {
                                doc.tipo = 'outro';
                            }
                            
                            dados.documentos.push(doc);
                            dados.links_pdf.push(url_completa);
                        }
                    });
                    
                    return dados;
                }
            """)
            
            dados_completos.update(resultado)
            
            # Salvar se solicitado
            if salvar_arquivos:
                nome_arquivo = numero_processo.replace(".", "_").replace("-", "_")
                output_dir = Path(__file__).parent
                output_dir.mkdir(exist_ok=True)
                
                arquivo = output_dir / f"processo_completo_{nome_arquivo}.json"
                with open(arquivo, 'w', encoding='utf-8') as f:
                    json.dump(dados_completos, f, indent=2, ensure_ascii=False)
                
                print(f"\n✅ Processo extraído completamente!")
                print(f"   📄 Arquivo: {arquivo}")
            
            print(f"\n📊 Estatísticas:")
            print(f"   • Movimentações: {len(dados_completos['movimentacoes'])}")
            print(f"   • Sentenças: {len(dados_completos['sentencas'])}")
            print(f"   • Julgados: {len(dados_completos['julgados'])}")
            print(f"   • Denúncias: {len(dados_completos['denuncias'])}")
            print(f"   • Documentos: {len(dados_completos['documentos'])}")
            print(f"   • Links PDF: {len(dados_completos['links_pdf'])}")
            print(f"   • Partes: {len(dados_completos['partes'])}")
            
            return dados_completos
            
        except Exception as e:
            print(f"❌ Erro durante extração: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            browser.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        numero = sys.argv[1]
    else:
        numero = "0878961-59.2013.8.13.0702"
        print(f"⚠️ Usando processo padrão: {numero}")
        print(f"   Para usar outro: python extrair_processo_completo.py <numero_processo>")
        print()
    
    resultado = extrair_processo_completo(numero)
    
    if resultado:
        print(f"\n✅ Extração concluída com sucesso!")

