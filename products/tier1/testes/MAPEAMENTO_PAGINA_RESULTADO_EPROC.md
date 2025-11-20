# 🗺️ Mapeamento Completo - Página de Resultado do Processo (eproc TJMG)

**Objetivo:** Extrair todos os dados possíveis da página de resultado:
- ✅ Sentenças
- ✅ Julgados
- ✅ Denúncias
- ✅ Documentos/Arquivos
- ✅ Movimentações
- ✅ Partes
- ✅ Histórico completo

---

## 📋 ESTRUTURA ESPERADA DA PÁGINA DE RESULTADO

Após buscar um processo, o eproc exibe uma página com várias seções:

```
┌─────────────────────────────────────────────────────────┐
│  DADOS DO PROCESSO                                      │
│  • Número                                               │
│  • Classe                                               │
│  • Vara/Turma                                           │
│  • Status                                               │
├─────────────────────────────────────────────────────────┤
│  PARTES                                                 │
│  • Autor/Réu                                            │
│  • Advogados                                            │
│  • Ministério Público                                    │
├─────────────────────────────────────────────────────────┤
│  MOVIMENTAÇÕES (Histórico)                             │
│  • Data | Tipo | Descrição                              │
│  • Sentenças                                            │
│  • Julgados                                             │
│  • Denúncias                                            │
├─────────────────────────────────────────────────────────┤
│  DOCUMENTOS/ARQUIVOS                                    │
│  • Links para PDFs                                      │
│  • Petições                                             │
│  • Sentenças (PDF)                                      │
│  • Denúncias (PDF)                                      │
└─────────────────────────────────────────────────────────┘
```

---

## 🔍 SELETORES COMUNS DE SISTEMAS EPROC

Baseado na estrutura padrão do sistema eproc, os seletores geralmente seguem este padrão:

### **1. CABEÇALHO/DADOS PRINCIPAIS**

```python
# Número do Processo
'.numero-processo, #numeroProcesso, .processo-numero'

# Classe do Processo
'.classe-processo, .classe, [data-field="classe"]'

# Vara/Turma
'.vara, .turma, .orgao-julgador'

# Status
'.status-processo, .situacao, .status'

# Data de Distribuição
'.data-distribuicao, .data'
```

### **2. PARTES**

```python
# Tabela de Partes
'table.partes, .lista-partes, #partes'

# Autor
'.parte-autor, .autor, [role="autor"]'

# Réu
'.parte-reu, .reu, [role="reu"]'

# Advogados
'.advogado, .parte-advogado, .representante'

# Ministério Público
'.ministerio-publico, .mp'
```

### **3. MOVIMENTAÇÕES/HISTÓRICO**

```python
# Lista de Movimentações
'.movimentacoes, .historico, #movimentacoes, table.movimentacao'

# Cada Movimentação
'.movimentacao-item, .item-movimentacao, tr.movimentacao'

# Data da Movimentação
'.data-movimentacao, .mov-data, td.data'

# Tipo da Movimentação
'.tipo-movimentacao, .mov-tipo, td.tipo'

# Descrição
'.descricao-movimentacao, .mov-descricao, td.descricao'

# Sentenças (filtro)
'.sentenca, .mov-sentenca, [data-tipo="sentenca"]'

# Julgados (filtro)
'.julgado, .mov-julgado, [data-tipo="julgado"]'

# Denúncias (filtro)
'.denuncia, .mov-denuncia, [data-tipo="denuncia"]'
```

### **4. DOCUMENTOS/ARQUIVOS**

```python
# Seção de Documentos
'.documentos, #documentos, .arquivos'

# Lista de Documentos
'.lista-documentos, table.documentos, #lista-documentos'

# Cada Documento
'.documento-item, .item-documento, tr.documento'

# Link para PDF/Documento
'a[href*=".pdf"], a.download, .link-documento'

# Tipo de Documento
'.tipo-documento, .doc-tipo'

# Data do Documento
'.data-documento, .doc-data'

# Descrição do Documento
'.descricao-documento, .doc-descricao'

# Links específicos:
# Sentença em PDF
'a[href*="sentenca"], a[href*="Sentenca"]'

# Denúncia em PDF
'a[href*="denuncia"], a[href*="Denuncia"]'

# Julgado em PDF
'a[href*="julgado"], a[href*="Julgado"]'
```

---

## 📝 SCRIPT PARA MAPEAR PÁGINA DE RESULTADO

```python
# kermartin/scripts/mapear_resultado_eproc.py

"""
Script para mapear estrutura completa da página de resultado do eproc
Execute após fazer uma busca real no eproc
"""

from playwright.sync_api import sync_playwright
import json

def mapear_pagina_resultado(numero_processo: str):
    """
    Faz busca real, captura página de resultado e mapeia todos os elementos
    """
    
    url_busca = "https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False para ver
        page = browser.new_page()
        
        # 1. Navegar e buscar
        page.goto(url_busca)
        page.fill('#txtNumProcesso', numero_processo)
        page.click('#sbmNovo')
        
        # 2. Aguardar página de resultado carregar
        page.wait_for_load_state('networkidle', timeout=30000)
        
        # 3. Mapear estrutura completa
        estrutura = page.evaluate("""
            () => {
                const resultado = {
                    // Dados principais
                    dados_principais: {},
                    partes: [],
                    movimentacoes: [],
                    documentos: [],
                    seletores_encontrados: []
                };
                
                // Mapear dados principais
                const possiveis_numeros = [
                    '.numero-processo', '#numeroProcesso', 
                    '.processo-numero', '[data-field="numero"]',
                    'h1', 'h2', '.titulo-processo'
                ];
                
                possiveis_numeros.forEach(sel => {
                    const el = document.querySelector(sel);
                    if (el && !resultado.dados_principais.numero) {
                        resultado.dados_principais.numero = el.innerText.trim();
                        resultado.seletores_encontrados.push({
                            tipo: 'numero',
                            seletor: sel,
                            texto: el.innerText.trim()
                        });
                    }
                });
                
                // Mapear tabelas de movimentação
                const tabelas = document.querySelectorAll('table');
                tabelas.forEach((table, idx) => {
                    const rows = table.querySelectorAll('tr');
                    if (rows.length > 1) {
                        resultado.seletores_encontrados.push({
                            tipo: 'tabela',
                            indice: idx,
                            seletor: `table:nth-of-type(${idx+1})`,
                            linhas: rows.length
                        });
                        
                        // Tentar identificar se é movimentação
                        const primeira_linha = rows[0].innerText.toLowerCase();
                        if ('data' in primeira_linha || 'movimenta' in primeira_linha || 'historico' in primeira_linha) {
                            resultado.seletores_encontrados.push({
                                tipo: 'tabela_movimentacao',
                                seletor: `table:nth-of-type(${idx+1})`
                            });
                        }
                    }
                });
                
                // Mapear links para documentos
                const links = document.querySelectorAll('a[href]');
                links.forEach(link => {
                    const href = link.getAttribute('href');
                    const texto = link.innerText.trim();
                    
                    if (href && (href.includes('.pdf') || href.includes('documento') || href.includes('Download'))) {
                        resultado.documentos.push({
                            texto: texto,
                            href: href,
                            seletor: 'a[href*="' + href.split('/').pop() + '"]'
                        });
                        
                        // Classificar por tipo
                        const textoLower = texto.toLowerCase();
                        if ('senten' in textoLower):
                            resultado.documentos[resultado.documentos.length - 1].tipo = 'sentenca';
                        elif ('denunci' in textoLower):
                            resultado.documentos[resultado.documentos.length - 1].tipo = 'denuncia';
                        elif ('julgado' in textoLower):
                            resultado.documentos[resultado.documentos.length - 1].tipo = 'julgado';
                    }
                });
                
                // Mapear todas as classes CSS únicas
                const todas_classes = new Set();
                document.querySelectorAll('[class]').forEach(el => {
                    el.className.split(' ').forEach(cls => {
                        if (cls && cls.length > 2) {
                            todas_classes.add(cls);
                        }
                    });
                });
                
                resultado.todas_classes_css = Array.from(todas_classes);
                
                return resultado;
            }
        """)
        
        # 4. Salvar mapeamento
        with open(f'mapeamento_resultado_{numero_processo.replace(".", "_")}.json', 'w') as f:
            json.dump(estrutura, f, indent=2, ensure_ascii=False)
        
        # 5. Capturar HTML completo (para análise)
        html = page.content()
        with open(f'html_resultado_{numero_processo.replace(".", "_")}.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        # 6. Screenshot para referência visual
        page.screenshot(path=f'screenshot_resultado_{numero_processo.replace(".", "_")}.png', full_page=True)
        
        browser.close()
        
        print(f"✅ Mapeamento salvo!")
        print(f"   JSON: mapeamento_resultado_{numero_processo.replace('.', '_')}.json")
        print(f"   HTML: html_resultado_{numero_processo.replace('.', '_')}.html")
        print(f"   Screenshot: screenshot_resultado_{numero_processo.replace('.', '_')}.png")

if __name__ == "__main__":
    numero_teste = "0878961-59.2013.8.13.0702"
    mapear_pagina_resultado(numero_teste)
```

---

## 🎯 EXTRAÇÃO COMPLETA DE DADOS

### **Script para Extrair TUDO:**

```python
# kermartin/scripts/extrair_processo_completo.py

from playwright.sync_api import sync_playwright
import json
from datetime import datetime

def extrair_processo_completo(numero_processo: str):
    """
    Extrai TODOS os dados possíveis de um processo:
    - Dados principais
    - Partes
    - Movimentações completas
    - Sentenças
    - Julgados  
    - Denúncias
    - Todos os documentos/arquivos
    """
    
    url_busca = "https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica"
    
    dados_completos = {
        'numero': numero_processo,
        'data_extração': datetime.now().isoformat(),
        'dados_principais': {},
        'partes': [],
        'movimentacoes': [],
        'sentencas': [],
        'julgados': [],
        'denuncias': [],
        'documentos': []
    }
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Buscar processo
        page.goto(url_busca)
        page.fill('#txtNumProcesso', numero_processo)
        page.click('#sbmNovo')
        page.wait_for_load_state('networkidle', timeout=30000)
        
        # Extrair tudo usando JavaScript
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
                
                // 1. DADOS PRINCIPAIS
                const buscar_texto = (seletores) => {
                    for (const sel of seletores) {
                        const el = document.querySelector(sel);
                        if (el) return el.innerText.trim();
                    }
                    return null;
                };
                
                dados.dados_principais = {
                    numero: buscar_texto(['.numero-processo', '#numeroProcesso', 'h1', 'h2']),
                    classe: buscar_texto(['.classe', '.tipo-processo']),
                    vara: buscar_texto(['.vara', '.turma', '.orgao-julgador']),
                    status: buscar_texto(['.status', '.situacao']),
                    comarca: buscar_texto(['.comarca'])
                };
                
                // 2. PARTES
                const tabela_partes = document.querySelector('table.partes, .lista-partes, table');
                if (tabela_partes) {
                    const linhas = tabela_partes.querySelectorAll('tr');
                    linhas.forEach(linha => {
                        const cols = linha.querySelectorAll('td, th');
                        if (cols.length >= 2) {
                            dados.partes.push({
                                tipo: cols[0]?.innerText.trim() || '',
                                nome: cols[1]?.innerText.trim() || '',
                                completo: linha.innerText.trim()
                            });
                        }
                    });
                }
                
                // 3. MOVIMENTAÇÕES
                const tabela_mov = document.querySelector('table.movimentacao, .historico table, #movimentacoes table');
                if (tabela_mov) {
                    const linhas = tabela_mov.querySelectorAll('tr');
                    linhas.forEach((linha, idx) => {
                        if (idx === 0) return; // Pular cabeçalho
                        
                        const cols = linha.querySelectorAll('td');
                        if (cols.length >= 3) {
                            const movimentacao = {
                                data: cols[0]?.innerText.trim() || '',
                                tipo: cols[1]?.innerText.trim() || '',
                                descricao: cols[2]?.innerText.trim() || '',
                                texto_completo: linha.innerText.trim()
                            };
                            
                            dados.movimentacoes.push(movimentacao);
                            
                            // Classificar por tipo
                            const tipoLower = movimentacao.tipo.toLowerCase();
                            if (tipoLower.includes('senten')) {
                                dados.sentencas.push(movimentacao);
                            }
                            if (tipoLower.includes('julgado') || tipoLower.includes('júri')) {
                                dados.julgados.push(movimentacao);
                            }
                            if (tipoLower.includes('denunci')) {
                                dados.denuncias.push(movimentacao);
                            }
                        }
                    });
                }
                
                // 4. DOCUMENTOS/ARQUIVOS
                const links = document.querySelectorAll('a[href]');
                links.forEach(link => {
                    const href = link.getAttribute('href');
                    const texto = link.innerText.trim();
                    
                    if (href && (
                        href.includes('.pdf') || 
                        href.includes('documento') || 
                        href.includes('Download') ||
                        href.includes('download') ||
                        href.includes('arquivo')
                    )) {
                        const doc = {
                            texto: texto,
                            href: href,
                            url_completa: href.startsWith('http') ? href : window.location.origin + href
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
                        }
                        
                        dados.documentos.push(doc);
                    }
                });
                
                return dados;
            }
        """)
        
        dados_completos.update(resultado)
        
        # Salvar
        arquivo = f"processo_completo_{numero_processo.replace('.', '_')}.json"
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados_completos, f, indent=2, ensure_ascii=False)
        
        browser.close()
        
        print(f"✅ Processo extraído completamente!")
        print(f"   Arquivo: {arquivo}")
        print(f"   Movimentações: {len(dados_completos['movimentacoes'])}")
        print(f"   Sentenças: {len(dados_completos['sentencas'])}")
        print(f"   Julgados: {len(dados_completos['julgados'])}")
        print(f"   Denúncias: {len(dados_completos['denuncias'])}")
        print(f"   Documentos: {len(dados_completos['documentos'])}")
        
        return dados_completos

if __name__ == "__main__":
    numero = "0878961-59.2013.8.13.0702"
    extrair_processo_completo(numero)
```

---

## 📊 DICIONÁRIO DE SELETORES ESPERADOS

```python
# kermartin/scripts/seletores_resultado_eproc.py

SELETORES_RESULTADO = {
    # Dados Principais
    'numero': ['.numero-processo', '#numeroProcesso', 'h1', '.titulo-processo'],
    'classe': ['.classe', '.tipo-processo', '[data-field="classe"]'],
    'vara': ['.vara', '.turma', '.orgao-julgador'],
    'status': ['.status', '.situacao', '[data-field="status"]'],
    'comarca': ['.comarca'],
    
    # Partes
    'tabela_partes': ['table.partes', '.lista-partes', '#partes table'],
    'autor': ['.parte-autor', '.autor', '[role="autor"]'],
    'reu': ['.parte-reu', '.reu', '[role="reu"]'],
    'advogado': ['.advogado', '.representante'],
    
    # Movimentações
    'tabela_movimentacoes': ['table.movimentacao', '.historico table', '#movimentacoes'],
    'item_movimentacao': ['tr.movimentacao', '.item-movimentacao', '.movimentacao-item'],
    'data_mov': ['td.data', '.data-movimentacao'],
    'tipo_mov': ['td.tipo', '.tipo-movimentacao'],
    'desc_mov': ['td.descricao', '.descricao-movimentacao'],
    
    # Filtros Específicos
    'sentenca': ['.sentenca', '[data-tipo="sentenca"]', 'tr:has-text("Sentença")'],
    'julgado': ['.julgado', '[data-tipo="julgado"]', 'tr:has-text("Julgado")'],
    'denuncia': ['.denuncia', '[data-tipo="denuncia"]', 'tr:has-text("Denúncia")'],
    
    # Documentos
    'secao_documentos': ['.documentos', '#documentos', '.arquivos'],
    'lista_documentos': ['table.documentos', '.lista-documentos'],
    'link_pdf': ['a[href*=".pdf"]', 'a.download', '.link-documento'],
    'link_sentenca': ['a[href*="sentenca"]', 'a[href*="Sentenca"]'],
    'link_denuncia': ['a[href*="denuncia"]', 'a[href*="Denuncia"]'],
    'link_julgado': ['a[href*="julgado"]', 'a[href*="Julgado"]'],
}
```

---

## 🚀 COMO USAR

### **1. Primeiro: Mapear estrutura real**

```bash
cd /home/clenio/Documentos/Meusagentes/kermartin/scripts

# Executar script de mapeamento
python mapear_resultado_eproc.py
```

Isso vai:
- Fazer busca real
- Capturar HTML
- Gerar screenshot
- Criar JSON com seletores encontrados

### **2. Depois: Ajustar seletores**

Analisar os arquivos gerados e ajustar os seletores no código.

### **3. Final: Usar na produção**

Copiar seletores validados para o script principal de coleta.

---

## ✅ CHECKLIST DE EXTRAÇÃO

Para garantir que tudo é extraído:

- [ ] Dados principais (número, classe, vara, status)
- [ ] Partes (autor, réu, advogados)
- [ ] Movimentações (todas)
- [ ] Sentenças (filtradas)
- [ ] Julgados (filtrados)
- [ ] Denúncias (filtradas)
- [ ] Documentos/Arquivos (links PDFs)
- [ ] Histórico completo
- [ ] Datas importantes
- [ ] Magistrado/Promotor

---

**Próximo passo:** Executar script de mapeamento com um processo real! 🎯

