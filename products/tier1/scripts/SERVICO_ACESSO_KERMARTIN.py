"""
Serviço para acessar dados do Kermartin
Permite consultar processos, magistrados e promotores já coletados
"""

import sys
import json
import sqlite3
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime

# Adiciona o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.utils.logger import bot_telegram_logger as logger

# Caminho base do Kermartin
KERMARTIN_BASE = Path("/home/clenio/Documentos/Meusagentes/kermartin")
KERMARTIN_DB = KERMARTIN_BASE / "db.sqlite3"
KERMARTIN_KB = KERMARTIN_BASE / "knowledge_base"
KERMARTIN_DATA = KERMARTIN_BASE / "data"


class KermartinService:
    """Serviço para acessar dados coletados no Kermartin"""
    
    def __init__(self):
        self.base_path = KERMARTIN_BASE
        self.db_path = KERMARTIN_DB
        self.kb_path = KERMARTIN_KB
        self.data_path = KERMARTIN_DATA
        
        # Verificar se caminhos existem
        if not self.base_path.exists():
            logger.warning(f"Caminho do Kermartin não encontrado: {self.base_path}")
        else:
            logger.info(f"✅ Serviço Kermartin inicializado: {self.base_path}")
    
    def buscar_magistrado(self, nome: str) -> Optional[Dict]:
        """
        Busca perfil de magistrado na base de conhecimento
        
        Args:
            nome: Nome do magistrado (pode ser parcial)
            
        Returns:
            Dict com dados do magistrado ou None
        """
        try:
            magistrados_path = self.kb_path / "magistrados"
            
            if not magistrados_path.exists():
                logger.warning("Diretório de magistrados não encontrado")
                return None
            
            # Buscar por nome (case-insensitive)
            nome_lower = nome.lower().strip()
            
            for arquivo in magistrados_path.glob("*.json"):
                try:
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        dados = json.load(f)
                    
                    # Verificar se nome corresponde
                    nome_magistrado = dados.get('nome_publico', '').lower()
                    nome_arquivo = arquivo.stem.lower()
                    
                    if nome_lower in nome_magistrado or nome_lower in nome_arquivo:
                        logger.info(f"Magistrado encontrado: {arquivo.stem}")
                        return dados
                        
                except Exception as e:
                    logger.warning(f"Erro ao ler {arquivo}: {e}")
                    continue
            
            logger.info(f"Magistrado '{nome}' não encontrado na base")
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar magistrado: {e}")
            return None
    
    def buscar_promotor(self, nome: str) -> Optional[Dict]:
        """
        Busca perfil de promotor na base de conhecimento
        """
        try:
            promotores_path = self.kb_path / "promotores"
            
            if not promotores_path.exists():
                return None
            
            nome_lower = nome.lower().strip()
            
            for arquivo in promotores_path.glob("*.json"):
                try:
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        dados = json.load(f)
                    
                    nome_promotor = dados.get('nome', '').lower()
                    nome_arquivo = arquivo.stem.lower()
                    
                    if nome_lower in nome_promotor or nome_lower in nome_arquivo:
                        logger.info(f"Promotor encontrado: {arquivo.stem}")
                        return dados
                        
                except Exception as e:
                    continue
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar promotor: {e}")
            return None
    
    def buscar_processos_por_comarca(self, comarca: str) -> List[Dict]:
        """
        Busca processos coletados por comarca
        
        Args:
            comarca: Nome da comarca (ex: "Uberlândia")
            
        Returns:
            Lista de processos encontrados
        """
        try:
            processos = []
            
            # Buscar em data/triangulo_mineiro/processos/
            triangulo_path = self.data_path / "triangulo_mineiro" / "processos"
            
            if triangulo_path.exists():
                for arquivo in triangulo_path.glob("*.json"):
                    try:
                        with open(arquivo, 'r', encoding='utf-8') as f:
                            dados = json.load(f)
                        
                        # Se for lista, processar cada item
                        if isinstance(dados, list):
                            for processo in dados:
                                if isinstance(processo, dict):
                                    if comarca.lower() in str(processo.get('comarca', '')).lower():
                                        processos.append(processo)
                        elif isinstance(dados, dict):
                            if comarca.lower() in str(dados.get('comarca', '')).lower():
                                processos.append(dados)
                                
                    except Exception as e:
                        continue
            
            logger.info(f"Encontrados {len(processos)} processos para {comarca}")
            return processos
            
        except Exception as e:
            logger.error(f"Erro ao buscar processos: {e}")
            return []
    
    def consultar_db_django(self, query: str, params: tuple = ()) -> List[Dict]:
        """
        Consulta direta no banco SQLite do Django
        
        Args:
            query: SQL query
            params: Parâmetros da query
            
        Returns:
            Lista de resultados
        """
        try:
            if not self.db_path.exists():
                logger.warning("Banco de dados do Kermartin não encontrado")
                return []
            
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Retornar como dict
            cursor = conn.cursor()
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # Converter para lista de dicts
            resultados = [dict(row) for row in rows]
            
            conn.close()
            return resultados
            
        except Exception as e:
            logger.error(f"Erro ao consultar banco: {e}")
            return []
    
    def buscar_processos_rag(self, filtro: Dict) -> List[Dict]:
        """
        Busca processos na base RAG do Django
        
        Args:
            filtro: Dict com filtros (tribunal, comarca, tipo, etc.)
            
        Returns:
            Lista de processos
        """
        try:
            # Construir query base
            query = "SELECT * FROM ai_engine_ragknowledgebase WHERE 1=1"
            params = []
            
            # Adicionar filtros
            if filtro.get('tribunal'):
                query += " AND metadata_json LIKE ?"
                params.append(f'%"tribunal":"{filtro["tribunal"]}%')
            
            if filtro.get('comarca'):
                query += " AND metadata_json LIKE ?"
                params.append(f'%"comarca":"{filtro["comarca"]}%')
            
            query += " LIMIT 50"  # Limitar resultados
            
            return self.consultar_db_django(query, tuple(params))
            
        except Exception as e:
            logger.error(f"Erro ao buscar processos RAG: {e}")
            return []
    
    def listar_magistrados_disponiveis(self, comarca: str = None) -> List[str]:
        """
        Lista todos os magistrados disponíveis na base
        
        Args:
            comarca: Filtrar por comarca (opcional)
            
        Returns:
            Lista de nomes de magistrados
        """
        try:
            magistrados = []
            magistrados_path = self.kb_path / "magistrados"
            
            if not magistrados_path.exists():
                return []
            
            for arquivo in magistrados_path.glob("*.json"):
                try:
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        dados = json.load(f)
                    
                    nome = dados.get('nome_publico') or dados.get('nome') or arquivo.stem
                    
                    # Filtrar por comarca se especificado
                    if comarca:
                        comarca_magistrado = dados.get('comarca', '').lower()
                        if comarca.lower() not in comarca_magistrado:
                            continue
                    
                    magistrados.append(nome)
                    
                except:
                    continue
            
            return sorted(set(magistrados))
            
        except Exception as e:
            logger.error(f"Erro ao listar magistrados: {e}")
            return []


# Instância global
kermartin_service = KermartinService()

