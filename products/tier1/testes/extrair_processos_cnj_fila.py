#!/usr/bin/env python3
"""
Script para extrair dados de processos via API CNJ em fila

Uso:
    python3 extrair_processos_cnj_fila.py processos.txt
    python3 extrair_processos_cnj_fila.py "0878961-59.2013.8.13.0702" "0001234-56.2024.8.26.0100"
"""

import sys
import os
import json
import time
import re
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

import requests


class CNJExtractor:
    """Extrator de dados de processos via API CNJ"""
    
    BASE_URL = "https://api-publica.datajud.cnj.jus.br"
    # Chave pública padrão fornecida pelo CNJ (pode mudar - verificar documentação)
    API_KEY_PUBLICA = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
    PROCESSO_PATTERN = re.compile(r'^(\d{7})-(\d{2})\.(\d{4})\.(\d)\.(\d{2})\.(\d{4})$')
    
    def __init__(self, delay_segundos: float = 1.0):
        """
        Args:
            delay_segundos: Tempo de espera entre requisições (respeitar rate limit)
        """
        self.delay = delay_segundos
        
        self.session = requests.Session()
        # API pública do CNJ - usa chave pública padrão
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'APIKey {self.API_KEY_PUBLICA}',
            'User-Agent': 'CNJ-Extractor/1.0'
        }
        
        self.session.headers.update(headers)
        self.resultados = []
        self.erros = []
    
    def validar_numero_processo(self, numero: str) -> bool:
        """Valida formato CNJ"""
        numero_limpo = numero.replace(' ', '').replace('-', '-').replace('.', '.')
        return bool(self.PROCESSO_PATTERN.match(numero_limpo))
    
    def formatar_numero_processo(self, numero: str) -> Optional[str]:
        """Formata número para padrão CNJ"""
        numero_limpo = re.sub(r'[^\d.-]', '', numero)
        
        if self.validar_numero_processo(numero_limpo):
            return numero_limpo
        
        # Tenta formatar removendo tudo e reconstruindo
        apenas_numeros = re.sub(r'[^\d]', '', numero_limpo)
        
        if len(apenas_numeros) >= 20:
            parte1 = apenas_numeros[:7]
            parte2 = apenas_numeros[7:9]
            parte3 = apenas_numeros[9:13]
            parte4 = apenas_numeros[13:14]
            parte5 = apenas_numeros[14:16]
            parte6 = apenas_numeros[16:20]
            
            formatado = f"{parte1}-{parte2}.{parte3}.{parte4}.{parte5}.{parte6}"
            if self.validar_numero_processo(formatado):
                return formatado
        
        return None
    
    def extrair_alias_tribunal(self, numero_formatado: str) -> str:
        """
        Extrai alias do tribunal do número do processo
        
        Formato: api_publica_tj{codigo}
        Exemplos: api_publica_tj26 (TJMG), api_publica_tj02 (TJSP)
        
        Formato CNJ: NNNNNNN-DD.AAAA.J.TR.OOOO
        - partes[0] = "NNNNNNN-DD"
        - partes[1] = "AAAA" (ano)
        - partes[2] = "J" (segmento: 8=Justiça Estadual)
        - partes[3] = "TR" (código do tribunal) ← AQUI!
        - partes[4] = "OOOO" (vara)
        """
        # Formato: NNNNNNN-DD.AAAA.J.TR.OOOO
        partes = numero_formatado.split('.')
        if len(partes) >= 4:
            codigo_tribunal = partes[3]  # TR está na posição 3
            return f"api_publica_tj{codigo_tribunal}"
        return "api_publica_tj26"  # Default: TJMG
    
    def classificar_movimentacao(self, descricao: str) -> Dict[str, bool]:
        """
        Classifica movimentação como sentença, julgado, denúncia, etc.
        
        Returns:
            Dict com flags de classificação
        """
        desc_lower = descricao.lower()
        
        return {
            'sentenca': any(palavra in desc_lower for palavra in [
                'sentença', 'sentenca', 'julgamento', 'decisão', 'decisao',
                'sentenciar', 'julgo', 'julgar'
            ]),
            'julgado': any(palavra in desc_lower for palavra in [
                'julgado', 'acórdão', 'acordao', 'recurso', 'apelação', 'apelacao',
                'agravo', 'embargos'
            ]),
            'denuncia': any(palavra in desc_lower for palavra in [
                'denúncia', 'denuncia', 'imputação', 'imputacao', 'acusação', 'acusacao'
            ]),
            'peticao': any(palavra in desc_lower for palavra in [
                'petição', 'peticao', 'requerimento', 'manifestação', 'manifestacao'
            ]),
            'despacho': any(palavra in desc_lower for palavra in [
                'despacho', 'determinação', 'determinacao', 'provimento'
            ]),
            'certidao': any(palavra in desc_lower for palavra in [
                'certidão', 'certidao', 'intimação', 'intimacao'
            ])
        }
    
    def buscar_processo(self, numero_processo: str) -> Optional[Dict]:
        """
        Busca processo na API CNJ
        
        Returns:
            Dict com dados completos do processo ou None se erro
        """
        # Validar e formatar
        numero_formatado = self.formatar_numero_processo(numero_processo)
        if not numero_formatado:
            return {
                'erro': f'Número inválido: {numero_processo}',
                'numero_original': numero_processo
            }
        
        # Extrair tribunal
        alias_tribunal = self.extrair_alias_tribunal(numero_formatado)
        
        # API CNJ - formato POST com query
        # URL: https://api-publica.datajud.cnj.jus.br/api_publica_tj26/_search
        url = f"{self.BASE_URL}/{alias_tribunal}/_search"
        
        # Payload para busca por número de processo
        payload = {
            "query": {
                "match": {
                    "numeroProcesso": numero_formatado
                }
            }
        }
        
        try:
            # API pública - requisição POST com query
            response = self.session.post(url, json=payload, timeout=15)
            
            if response.status_code == 200:
                dados_json = response.json()
                # API retorna no formato Elasticsearch (_search)
                # Dados estão em hits.hits[0]._source
                if 'hits' in dados_json and 'hits' in dados_json['hits']:
                    hits = dados_json['hits']['hits']
                    if hits and len(hits) > 0:
                        dados = hits[0].get('_source', {})
                        return self.processar_dados_processo(dados, numero_formatado)
                    else:
                        return {
                            'erro': 'Processo não encontrado na API CNJ (sem resultados)',
                            'numero_formatado': numero_formatado,
                            'numero_original': numero_processo
                        }
                else:
                    # Tenta processar diretamente (caso estrutura diferente)
                    return self.processar_dados_processo(dados_json, numero_formatado)
            elif response.status_code == 404:
                return {
                    'erro': 'Processo não encontrado na API CNJ',
                    'numero_formatado': numero_formatado,
                    'numero_original': numero_processo,
                    'status_code': 404
                }
            elif response.status_code == 429:
                return {
                    'erro': 'Rate limit excedido (muitas requisições)',
                    'numero_formatado': numero_formatado,
                    'numero_original': numero_processo,
                    'status_code': 429
                }
            else:
                return {
                    'erro': f'Erro HTTP {response.status_code}',
                    'numero_formatado': numero_formatado,
                    'numero_original': numero_processo,
                    'status_code': response.status_code,
                    'resposta': response.text[:500]
                }
                
        except requests.exceptions.Timeout:
            return {
                'erro': 'Timeout na requisição',
                'numero_formatado': numero_formatado,
                'numero_original': numero_processo
            }
        except requests.exceptions.ConnectionError:
            return {
                'erro': 'Erro de conexão',
                'numero_formatado': numero_formatado,
                'numero_original': numero_processo
            }
        except Exception as e:
            return {
                'erro': f'Erro inesperado: {str(e)}',
                'numero_formatado': numero_formatado,
                'numero_original': numero_processo
            }
    
    def processar_dados_processo(self, dados_api: Dict, numero_formatado: str) -> Dict:
        """
        Processa e estrutura dados do processo
        
        Extrai:
        - Dados principais
        - Movimentações (todas, classificadas)
        - Partes
        - Sentenças, julgados, denúncias identificados
        """
        resultado = {
            'numero_processo': numero_formatado,
            'fonte': 'API CNJ DataJud',
            'data_extracao': datetime.now().isoformat(),
            'dados_principais': {},
            'movimentacoes': [],
            'movimentacoes_classificadas': {
                'sentencas': [],
                'julgados': [],
                'denuncias': [],
                'peticoes': [],
                'despachos': [],
                'certidoes': []
            },
            'partes': [],
            'estatisticas': {
                'total_movimentacoes': 0,
                'total_partes': 0,
                'total_sentencas': 0,
                'total_julgados': 0,
                'total_denuncias': 0
            }
        }
        
        # Dados principais
        resultado['dados_principais'] = {
            'numero': dados_api.get('numeroProcesso', numero_formatado),
            'classe': self._extrair_valor(dados_api.get('classe')),
            'assunto': self._extrair_assunto(dados_api.get('assunto')),
            'tribunal': self._extrair_valor(dados_api.get('tribunal')),
            'vara': dados_api.get('vara', dados_api.get('orgaoJulgador', 'N/A')),
            'status': dados_api.get('status', 'N/A'),
            'data_autuacao': dados_api.get('dataAbertura', dados_api.get('dataAutuacao', 'N/A')),
            'segredo_justica': dados_api.get('segredoJustica', False)
        }
        
        # Movimentações
        movimentacoes_raw = dados_api.get('movimentacoes', dados_api.get('movimentos', []))
        
        if isinstance(movimentacoes_raw, list):
            for mov in movimentacoes_raw:
                if isinstance(mov, dict):
                    mov_processada = {
                        'data': mov.get('data', mov.get('dataHora', 'N/A')),
                        'descricao': mov.get('descricao', mov.get('texto', 'N/A')),
                        'tipo': mov.get('tipo', 'N/A'),
                        'orgao': mov.get('orgao', mov.get('orgaoJulgador', 'N/A'))
                    }
                    
                    resultado['movimentacoes'].append(mov_processada)
                    
                    # Classificar movimentação
                    descricao = mov_processada['descricao']
                    classificacao = self.classificar_movimentacao(descricao)
                    
                    if classificacao['sentenca']:
                        resultado['movimentacoes_classificadas']['sentencas'].append(mov_processada)
                    if classificacao['julgado']:
                        resultado['movimentacoes_classificadas']['julgados'].append(mov_processada)
                    if classificacao['denuncia']:
                        resultado['movimentacoes_classificadas']['denuncias'].append(mov_processada)
                    if classificacao['peticao']:
                        resultado['movimentacoes_classificadas']['peticoes'].append(mov_processada)
                    if classificacao['despacho']:
                        resultado['movimentacoes_classificadas']['despachos'].append(mov_processada)
                    if classificacao['certidao']:
                        resultado['movimentacoes_classificadas']['certidoes'].append(mov_processada)
        
        # Partes
        partes_raw = dados_api.get('partes', dados_api.get('participantes', []))
        
        if isinstance(partes_raw, list):
            for parte in partes_raw:
                if isinstance(parte, dict):
                    parte_processada = {
                        'nome': parte.get('nome', parte.get('razaoSocial', 'N/A')),
                        'tipo': parte.get('tipo', parte.get('polo', 'N/A')),
                        'documento': parte.get('documento', parte.get('cpfCnpj', 'N/A')),
                        'polo': parte.get('polo', parte.get('tipoParticipacao', 'N/A'))
                    }
                    resultado['partes'].append(parte_processada)
        
        # Atualizar estatísticas
        resultado['estatisticas'] = {
            'total_movimentacoes': len(resultado['movimentacoes']),
            'total_partes': len(resultado['partes']),
            'total_sentencas': len(resultado['movimentacoes_classificadas']['sentencas']),
            'total_julgados': len(resultado['movimentacoes_classificadas']['julgados']),
            'total_denuncias': len(resultado['movimentacoes_classificadas']['denuncias'])
        }
        
        return resultado
    
    def _extrair_valor(self, obj) -> str:
        """Extrai valor de objeto (string ou dict)"""
        if isinstance(obj, str):
            return obj
        elif isinstance(obj, dict):
            return obj.get('nome', obj.get('descricao', 'N/A'))
        return 'N/A'
    
    def _extrair_assunto(self, assunto) -> str:
        """Extrai assunto (pode ser string, lista ou dict)"""
        if isinstance(assunto, str):
            return assunto
        elif isinstance(assunto, list) and assunto:
            if isinstance(assunto[0], dict):
                return assunto[0].get('nome', 'N/A')
            return str(assunto[0])
        elif isinstance(assunto, dict):
            return assunto.get('nome', 'N/A')
        return 'N/A'
    
    def processar_fila(self, processos: List[str], salvar_individual: bool = True) -> Dict:
        """
        Processa lista de processos em fila
        
        Args:
            processos: Lista de números de processos
            salvar_individual: Se True, salva cada processo em arquivo separado
        
        Returns:
            Dict com resumo da execução
        """
        total = len(processos)
        print(f"\n{'='*60}")
        print(f"🚀 PROCESSANDO {total} PROCESSO(S) EM FILA")
        print(f"{'='*60}\n")
        
        output_dir = Path(__file__).parent / 'extracao_cnj'
        output_dir.mkdir(exist_ok=True)
        
        sucessos = 0
        erros = 0
        
        for idx, processo in enumerate(processos, 1):
            processo_limpo = processo.strip()
            if not processo_limpo:
                continue
            
            print(f"[{idx}/{total}] 📄 Processando: {processo_limpo}")
            
            # Buscar processo
            resultado = self.buscar_processo(processo_limpo)
            
            if resultado and 'erro' not in resultado:
                sucessos += 1
                self.resultados.append(resultado)
                
                print(f"   ✅ Sucesso! Movimentações: {resultado['estatisticas']['total_movimentacoes']}")
                print(f"      • Sentenças: {resultado['estatisticas']['total_sentencas']}")
                print(f"      • Julgados: {resultado['estatisticas']['total_julgados']}")
                print(f"      • Denúncias: {resultado['estatisticas']['total_denuncias']}")
                
                # Salvar individual
                if salvar_individual:
                    nome_arquivo = processo_limpo.replace('.', '_').replace('-', '_')
                    arquivo_json = output_dir / f"processo_{nome_arquivo}.json"
                    with open(arquivo_json, 'w', encoding='utf-8') as f:
                        json.dump(resultado, f, indent=2, ensure_ascii=False)
                    print(f"      💾 Salvo: {arquivo_json.name}")
                    
            else:
                erros += 1
                erro_msg = resultado.get('erro', 'Erro desconhecido') if resultado else 'Sem resposta'
                self.erros.append({
                    'processo': processo_limpo,
                    'erro': erro_msg
                })
                print(f"   ❌ Erro: {erro_msg}")
            
            # Delay entre requisições
            if idx < total:
                print(f"   ⏳ Aguardando {self.delay}s...\n")
                time.sleep(self.delay)
        
        # Salvar resumo
        resumo = {
            'data_execucao': datetime.now().isoformat(),
            'total_processos': total,
            'sucessos': sucessos,
            'erros': erros,
            'resultados': self.resultados,
            'erros_detalhados': self.erros
        }
        
        arquivo_resumo = output_dir / f"resumo_extracao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(arquivo_resumo, 'w', encoding='utf-8') as f:
            json.dump(resumo, f, indent=2, ensure_ascii=False)
        
        # Exibir resumo
        print(f"\n{'='*60}")
        print(f"📊 RESUMO DA EXECUÇÃO")
        print(f"{'='*60}")
        print(f"✅ Sucessos: {sucessos}/{total}")
        print(f"❌ Erros: {erros}/{total}")
        print(f"📄 Resumo salvo: {arquivo_resumo.name}")
        print(f"{'='*60}\n")
        
        return resumo


def carregar_processos(entrada: str) -> List[str]:
    """Carrega lista de processos de arquivo ou string"""
    path = Path(entrada)
    
    if path.exists() and path.is_file():
        # Arquivo
        with open(path, 'r', encoding='utf-8') as f:
            processos = [linha.strip() for linha in f if linha.strip()]
        print(f"📂 Carregados {len(processos)} processos de: {path.name}")
        return processos
    else:
        # String direta (número do processo)
        return [entrada]


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("""
📋 Uso:
    python3 extrair_processos_cnj_fila.py <arquivo.txt>
    python3 extrair_processos_cnj_fila.py "processo1" "processo2" ...
    
Exemplos:
    python3 extrair_processos_cnj_fila.py processos.txt
    python3 extrair_processos_cnj_fila.py "0878961-59.2013.8.13.0702"
    python3 extrair_processos_cnj_fila.py "proc1" "proc2" "proc3"
        """)
        sys.exit(1)
    
    # Carregar processos
    processos = []
    for arg in sys.argv[1:]:
        processos.extend(carregar_processos(arg))
    
    if not processos:
        print("❌ Nenhum processo encontrado!")
        sys.exit(1)
    
    # Criar extrator
    # Delay de 1 segundo entre requisições (ajustar conforme necessário)
    extrator = CNJExtractor(delay_segundos=1.0)
    
    # Processar fila
    extrator.processar_fila(processos, salvar_individual=True)


if __name__ == '__main__':
    main()

