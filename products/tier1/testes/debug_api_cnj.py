#!/usr/bin/env python3
"""
Script de debug para ver respostas brutas da API CNJ
Mostra exatamente o que a API retorna, mesmo em caso de erro
"""

import sys
import json
import requests
import re
from typing import Optional, Dict

class CNJDebugger:
    """Debugger para API CNJ - mostra respostas brutas"""
    
    BASE_URL = "https://api-publica.datajud.cnj.jus.br"
    API_KEY_PUBLICA = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
    PROCESSO_PATTERN = re.compile(r'^(\d{7})-(\d{2})\.(\d{4})\.(\d)\.(\d{2})\.(\d{4})$')
    
    def __init__(self):
        self.session = requests.Session()
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'APIKey {self.API_KEY_PUBLICA}',
            'User-Agent': 'CNJ-Debugger/1.0'
        }
        self.session.headers.update(headers)
    
    def formatar_numero_processo(self, numero: str) -> Optional[str]:
        """Formata número para padrão CNJ"""
        numero_limpo = re.sub(r'[^\d.-]', '', numero)
        
        if self.PROCESSO_PATTERN.match(numero_limpo):
            return numero_limpo
        
        apenas_numeros = re.sub(r'[^\d]', '', numero_limpo)
        
        if len(apenas_numeros) >= 20:
            parte1 = apenas_numeros[:7]
            parte2 = apenas_numeros[7:9]
            parte3 = apenas_numeros[9:13]
            parte4 = apenas_numeros[13:14]
            parte5 = apenas_numeros[14:16]
            parte6 = apenas_numeros[16:20]
            
            formatado = f"{parte1}-{parte2}.{parte3}.{parte4}.{parte5}.{parte6}"
            if self.PROCESSO_PATTERN.match(formatado):
                return formatado
        
        return None
    
    def extrair_alias_tribunal(self, numero_formatado: str) -> str:
        """
        Extrai alias do tribunal do número do processo
        
        Formato CNJ: NNNNNNN-DD.AAAA.J.TR.OOOO
        - partes[3] = "TR" (código do tribunal) ← AQUI!
        """
        partes = numero_formatado.split('.')
        if len(partes) >= 4:
            codigo_tribunal = partes[3]  # TR está na posição 3
            return f"api_publica_tj{codigo_tribunal}"
        return "api_publica_tj26"
    
    def debug_processo(self, numero_processo: str) -> Dict:
        """
        Debug completo - mostra tudo que a API retorna
        """
        print("=" * 80)
        print(f"🔍 DEBUG API CNJ - Processo: {numero_processo}")
        print("=" * 80)
        
        # Validar e formatar
        numero_formatado = self.formatar_numero_processo(numero_processo)
        if not numero_formatado:
            print(f"❌ Número inválido: {numero_processo}")
            return {'erro': 'Número inválido'}
        
        print(f"✅ Número formatado: {numero_formatado}")
        
        # Extrair tribunal
        alias_tribunal = self.extrair_alias_tribunal(numero_formatado)
        print(f"🏛️  Tribunal alias: {alias_tribunal}")
        
        # Construir URL e payload
        url = f"{self.BASE_URL}/{alias_tribunal}/_search"
        payload = {
            "query": {
                "match": {
                    "numeroProcesso": numero_formatado
                }
            }
        }
        
        print(f"\n📡 Requisição:")
        print(f"   URL: {url}")
        print(f"   Método: POST")
        print(f"   Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")
        print(f"\n📤 Headers:")
        for key, value in self.session.headers.items():
            if key != 'Authorization':
                print(f"   {key}: {value}")
            else:
                print(f"   {key}: APIKey ***")
        
        try:
            print(f"\n⏳ Enviando requisição...")
            response = self.session.post(url, json=payload, timeout=15)
            
            print(f"\n📥 Resposta:")
            print(f"   Status Code: {response.status_code}")
            print(f"   Headers: {dict(response.headers)}")
            
            # Tentar parsear JSON
            try:
                dados_json = response.json()
                print(f"\n📄 Resposta JSON (completa):")
                print(json.dumps(dados_json, indent=2, ensure_ascii=False))
                
                # Analisar estrutura
                print(f"\n🔬 Análise da Estrutura:")
                if isinstance(dados_json, dict):
                    print(f"   Tipo: Dicionário")
                    print(f"   Chaves principais: {list(dados_json.keys())}")
                    
                    if 'hits' in dados_json:
                        hits = dados_json.get('hits', {})
                        print(f"   ✅ Estrutura Elasticsearch encontrada!")
                        print(f"   Total de hits: {hits.get('total', {}).get('value', 0)}")
                        
                        hits_list = hits.get('hits', [])
                        if hits_list:
                            print(f"   ✅ Processo encontrado!")
                            primeiro_hit = hits_list[0]
                            source = primeiro_hit.get('_source', {})
                            print(f"   Chaves em _source: {list(source.keys())[:10]}...")
                            
                            # Mostrar alguns campos importantes
                            print(f"\n📋 Dados Principais do Processo:")
                            print(f"   Número: {source.get('numeroProcesso', 'N/A')}")
                            print(f"   Classe: {source.get('classe', 'N/A')}")
                            print(f"   Tribunal: {source.get('tribunal', 'N/A')}")
                            print(f"   Vara: {source.get('vara', source.get('orgaoJulgador', 'N/A'))}")
                            
                            # Movimentações
                            movimentacoes = source.get('movimentacoes', source.get('movimentos', []))
                            if movimentacoes:
                                print(f"   Movimentações: {len(movimentacoes)} encontradas")
                                if len(movimentacoes) > 0:
                                    print(f"   Primeira movimentação: {movimentacoes[0]}")
                            
                            # Partes
                            partes = source.get('partes', source.get('participantes', []))
                            if partes:
                                print(f"   Partes: {len(partes)} encontradas")
                        else:
                            print(f"   ❌ Nenhum processo encontrado (hits vazio)")
                    else:
                        print(f"   ⚠️  Estrutura diferente do esperado")
                        print(f"   Chaves disponíveis: {list(dados_json.keys())}")
                else:
                    print(f"   Tipo: {type(dados_json)}")
                
            except json.JSONDecodeError:
                print(f"\n❌ Resposta não é JSON válido")
                print(f"   Primeiros 500 caracteres:")
                print(response.text[:500])
            
            return {
                'status_code': response.status_code,
                'response': dados_json if response.status_code == 200 else response.text[:1000],
                'numero_formatado': numero_formatado
            }
            
        except requests.exceptions.Timeout:
            print(f"\n❌ Timeout na requisição")
            return {'erro': 'Timeout'}
        except requests.exceptions.ConnectionError as e:
            print(f"\n❌ Erro de conexão: {e}")
            return {'erro': f'Erro de conexão: {e}'}
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            import traceback
            traceback.print_exc()
            return {'erro': str(e)}


def main():
    if len(sys.argv) < 2:
        print("""
🔍 Debug API CNJ - Ver respostas brutas da API

Uso:
    python3 debug_api_cnj.py <numero_processo>

Exemplo:
    python3 debug_api_cnj.py "0878961-59.2013.8.13.0702"
        """)
        sys.exit(1)
    
    numero_processo = sys.argv[1]
    debugger = CNJDebugger()
    resultado = debugger.debug_processo(numero_processo)
    
    print("\n" + "=" * 80)
    print("✅ Debug concluído!")
    print("=" * 80)


if __name__ == '__main__':
    main()

