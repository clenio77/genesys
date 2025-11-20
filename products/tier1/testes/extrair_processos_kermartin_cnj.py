#!/usr/bin/env python3
"""
Script para buscar processos do Kermartin e extrair via API CNJ

Extrai números de processos do Kermartin e testa extração completa via API CNJ
"""

import sys
import json
import sqlite3
from pathlib import Path
from typing import List, Set
import re

# Importar o extrator CNJ
from extrair_processos_cnj_fila import CNJExtractor


# Caminhos do Kermartin
KERMARTIN_BASE = Path("/home/clenio/Documentos/Meusagentes/kermartin")
KERMARTIN_DB = KERMARTIN_BASE / "db.sqlite3"
KERMARTIN_DATA = KERMARTIN_BASE / "data"
KERMARTIN_KB = KERMARTIN_BASE / "knowledge_base"

# Padrão CNJ
PROCESSO_PATTERN = re.compile(r'(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})')


def normalizar_numero_processo(texto: str) -> str:
    """Normaliza número de processo para formato CNJ"""
    # Remove espaços e caracteres extras
    texto = texto.replace(' ', '').replace('_', '').replace('-', '-').replace('.', '.')
    # Tenta encontrar padrão CNJ
    match = PROCESSO_PATTERN.search(texto)
    if match:
        return match.group(1)
    return texto.strip()


def extrair_processos_do_db() -> Set[str]:
    """Extrai números de processos do banco SQLite do Kermartin"""
    processos = set()
    
    if not KERMARTIN_DB.exists():
        print(f"⚠️  Banco SQLite não encontrado: {KERMARTIN_DB}")
        return processos
    
    try:
        conn = sqlite3.connect(str(KERMARTIN_DB))
        cursor = conn.cursor()
        
        # Tabela notifications_processo
        try:
            cursor.execute("SELECT numero_processo FROM notifications_processo WHERE numero_processo IS NOT NULL LIMIT 1000")
            rows = cursor.fetchall()
            for row in rows:
                if row[0]:
                    num_normalizado = normalizar_numero_processo(str(row[0]))
                    if PROCESSO_PATTERN.match(num_normalizado):
                        processos.add(num_normalizado)
        except Exception as e:
            print(f"⚠️  Erro ao ler notifications_processo: {e}")
        
        # Tabela tribunals_consultaprocesso (se existir)
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tribunals_consultaprocesso'")
            if cursor.fetchone():
                cursor.execute("SELECT numero_processo FROM tribunals_consultaprocesso WHERE numero_processo IS NOT NULL LIMIT 1000")
                rows = cursor.fetchall()
                for row in rows:
                    if row[0]:
                        num_normalizado = normalizar_numero_processo(str(row[0]))
                        if PROCESSO_PATTERN.match(num_normalizado):
                            processos.add(num_normalizado)
        except Exception as e:
            print(f"⚠️  Tabela tribunals_consultaprocesso não encontrada ou erro: {e}")
        
        conn.close()
        print(f"✅ Extraídos {len(processos)} processos únicos do banco SQLite")
        
    except Exception as e:
        print(f"❌ Erro ao acessar banco: {e}")
    
    return processos


def extrair_processos_dos_json() -> Set[str]:
    """Extrai números de processos dos arquivos JSON do Kermartin"""
    processos = set()
    
    # Buscar em vários diretórios possíveis
    diretorios_json = [
        KERMARTIN_DATA / "triangulo_mineiro" / "processos",
        KERMARTIN_DATA / "processos_mg",
        KERMARTIN_DATA / "processos",
    ]
    
    for diretorio in diretorios_json:
        if diretorio.exists():
            print(f"📂 Buscando em: {diretorio}")
            break
    else:
        # Se nenhum diretório específico existir, buscar em data/ recursivamente
        if KERMARTIN_DATA.exists():
            diretorios_json = [KERMARTIN_DATA]
        else:
            print(f"⚠️  Diretório data não encontrado: {KERMARTIN_DATA}")
            return processos
    
    arquivos_processados = 0
    for diretorio in diretorios_json:
        if not diretorio.exists():
            continue
        for arquivo in diretorio.rglob("*.json"):
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                arquivos_processados += 1
                
                # Se for lista
                if isinstance(dados, list):
                    for item in dados:
                        if isinstance(item, dict):
                            # Buscar em vários campos possíveis
                            for campo in ['numero', 'numero_cnj', 'numeroProcesso', 'processo', 'cnj', 'numero_processo']:
                                valor = item.get(campo)
                                if valor:
                                    num_normalizado = normalizar_numero_processo(str(valor))
                                    if PROCESSO_PATTERN.match(num_normalizado):
                                        processos.add(num_normalizado)
                # Se for dict único
                elif isinstance(dados, dict):
                    for campo in ['numero', 'numero_cnj', 'numeroProcesso', 'processo', 'cnj', 'numero_processo']:
                        valor = dados.get(campo)
                        if valor:
                            num_normalizado = normalizar_numero_processo(str(valor))
                            if PROCESSO_PATTERN.match(num_normalizado):
                                processos.add(num_normalizado)
                                
            except Exception as e:
                continue
    
    print(f"✅ Extraídos {len(processos)} processos únicos de {arquivos_processados} arquivos JSON")
    return processos


def extrair_processos_do_kb() -> Set[str]:
    """Extrai números de processos dos arquivos JSON da knowledge base"""
    processos = set()
    
    # Buscar em knowledge_base/processos/ se existir
    processos_path = KERMARTIN_KB / "processos"
    
    if not processos_path.exists():
        return processos
    
    for arquivo in processos_path.glob("*.json"):
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            # Buscar em vários campos
            if isinstance(dados, dict):
                for campo in ['numero', 'numero_cnj', 'numeroProcesso', 'processo', 'cnj']:
                    valor = dados.get(campo)
                    if valor:
                        num_normalizado = normalizar_numero_processo(str(valor))
                        if PROCESSO_PATTERN.match(num_normalizado):
                            processos.add(num_normalizado)
                            
        except Exception as e:
            continue
    
    print(f"✅ Extraídos {len(processos)} processos únicos da knowledge base")
    return processos


def coletar_processos_kermartin(limite: int = None) -> List[str]:
    """
    Coleta todos os números de processos do Kermartin
    
    Args:
        limite: Limitar número de processos (None = todos)
    
    Returns:
        Lista de números de processos únicos
    """
    print(f"\n{'='*60}")
    print(f"🔍 COLETANDO PROCESSOS DO KERMARTIN")
    print(f"{'='*60}\n")
    
    processos = set()
    
    # 1. Banco SQLite
    processos.update(extrair_processos_do_db())
    
    # 2. Arquivos JSON em data/
    processos.update(extrair_processos_dos_json())
    
    # 3. Knowledge base
    processos.update(extrair_processos_do_kb())
    
    # Converter para lista ordenada
    lista_processos = sorted(list(processos))
    
    if limite:
        lista_processos = lista_processos[:limite]
    
    print(f"\n📊 TOTAL: {len(lista_processos)} processos únicos encontrados")
    
    return lista_processos


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Extrair processos do Kermartin e buscar na API CNJ')
    parser.add_argument('-l', '--limite', type=int, default=10,
                        help='Limitar número de processos (padrão: 10)')
    parser.add_argument('-s', '--salvar-lista', action='store_true',
                        help='Salvar lista de processos em arquivo')
    parser.add_argument('--arquivo-lista', type=str,
                        help='Usar lista de processos de arquivo (ao invés de coletar)')
    
    args = parser.parse_args()
    
    # Obter lista de processos
    if args.arquivo_lista:
        print(f"📂 Carregando processos de: {args.arquivo_lista}")
        with open(args.arquivo_lista, 'r', encoding='utf-8') as f:
            processos = [linha.strip() for linha in f if linha.strip()]
        print(f"✅ {len(processos)} processos carregados")
    else:
        processos = coletar_processos_kermartin(limite=args.limite)
        
        # Salvar lista se solicitado
        if args.salvar_lista:
            arquivo_lista = Path(__file__).parent / f"processos_kermartin_{len(processos)}.txt"
            with open(arquivo_lista, 'w', encoding='utf-8') as f:
                for proc in processos:
                    f.write(f"{proc}\n")
            print(f"💾 Lista salva: {arquivo_lista}")
    
    if not processos:
        print("❌ Nenhum processo encontrado no Kermartin!")
        return
    
    # Executar extração via API CNJ
    print(f"\n{'='*60}")
    print(f"🚀 INICIANDO EXTRAÇÃO VIA API CNJ")
    print(f"{'='*60}\n")
    
    extrator = CNJExtractor(delay_segundos=1.0)
    resumo = extrator.processar_fila(processos, salvar_individual=True)
    
    # Estatísticas finais
    print(f"\n{'='*60}")
    print(f"📊 RESUMO FINAL")
    print(f"{'='*60}")
    print(f"✅ Processos processados com sucesso: {resumo['sucessos']}")
    print(f"❌ Processos com erro: {resumo['erros']}")
    print(f"📄 Total analisado: {len(processos)}")
    
    if resumo['sucessos'] > 0:
        print(f"\n💡 {resumo['sucessos']} processos foram extraídos com sucesso!")
        print(f"   Verifique os arquivos em: extracao_cnj/")


if __name__ == '__main__':
    main()

