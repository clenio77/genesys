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
    
    def _normalizar_nome(self, nome: str) -> str:
        """
        Normaliza nome para comparação:
        - Remove acentos
        - Converte para minúsculas
        - Remove espaços extras
        """
        import unicodedata
        # Converter para minúsculas e remover espaços extras
        nome = nome.lower().strip()
        # Remover acentos
        nome = unicodedata.normalize('NFD', nome)
        nome = ''.join(char for char in nome if unicodedata.category(char) != 'Mn')
        return nome
    
    def _buscar_nome_em_dados(self, nome_busca: str, dados: Dict) -> bool:
        """
        Busca nome normalizado em vários campos do magistrado
        """
        nome_busca_norm = self._normalizar_nome(nome_busca)
        
        # Campos possíveis onde o nome pode estar
        campos_nome = [
            dados.get('dados', {}).get('magistrado'),
            dados.get('metadata', {}).get('nome_magistrado'),
            dados.get('nome_publico'),
            dados.get('nome'),
        ]
        
        # Também verificar o nome do arquivo (já normalizado no loop)
        arquivo_nome = dados.get('_arquivo_nome', '')
        
        for campo in campos_nome:
            if campo:
                campo_norm = self._normalizar_nome(str(campo))
                # Busca exata ou parcial
                if nome_busca_norm == campo_norm or nome_busca_norm in campo_norm or campo_norm in nome_busca_norm:
                    return True
        
        # Verificar também no nome do arquivo
        if arquivo_nome:
            arquivo_norm = self._normalizar_nome(arquivo_nome)
            if nome_busca_norm in arquivo_norm or arquivo_norm in nome_busca_norm:
                return True
        
        return False
    
    def buscar_magistrado(self, nome: str) -> Optional[Dict]:
        """
        Busca perfil de magistrado na base de conhecimento
        
        Args:
            nome: Nome do magistrado (pode ser parcial, case-insensitive)
            
        Returns:
            Dict com dados do magistrado ou None
        """
        try:
            magistrados_path = self.kb_path / "magistrados"
            
            if not magistrados_path.exists():
                logger.warning("Diretório de magistrados não encontrado")
                return None
            
            # Normalizar nome de busca
            nome_busca_norm = self._normalizar_nome(nome)
            logger.info(f"Buscando magistrado: '{nome}' (normalizado: '{nome_busca_norm}')")
            
            # Lista para armazenar correspondências (pode ter múltiplas)
            correspondencias = []
            
            for arquivo in magistrados_path.glob("*.json"):
                try:
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        dados = json.load(f)
                    
                    # Adicionar nome do arquivo aos dados para busca
                    dados['_arquivo_nome'] = arquivo.stem
                    
                    # Verificar se nome corresponde
                    if self._buscar_nome_em_dados(nome, dados):
                        logger.info(f"✅ Magistrado encontrado: {arquivo.stem}")
                        correspondencias.append((arquivo.stem, dados))
                        
                except Exception as e:
                    logger.warning(f"Erro ao ler {arquivo}: {e}")
                    continue
            
            if correspondencias:
                # Se múltiplas correspondências, retornar a primeira (mais completa)
                # Ou a que tem o nome mais exato
                melhor_match = correspondencias[0][1]
                
                # Se tiver mais de uma, tentar encontrar a melhor correspondência
                if len(correspondencias) > 1:
                    for nome_arquivo, dados_match in correspondencias:
                        nome_magistrado = self._normalizar_nome(
                            dados_match.get('dados', {}).get('magistrado') or 
                            dados_match.get('metadata', {}).get('nome_magistrado') or 
                            nome_arquivo
                        )
                        # Priorizar correspondências exatas
                        if nome_busca_norm == nome_magistrado:
                            melhor_match = dados_match
                            logger.info(f"Melhor match encontrado: {nome_arquivo}")
                            break
                
                return melhor_match
            
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
    
    def buscar_processos_por_comarca(self, comarca: str, filtros: Optional[Dict] = None) -> List[Dict]:
        """
        Busca processos coletados por comarca com filtros opcionais
        
        Args:
            comarca: Nome da comarca (ex: "Uberlândia" ou "Uberlandia")
            filtros: Dict com filtros (tipo, status, limite)
            
        Returns:
            Lista de processos encontrados
            
        Nota: A busca ignora acentos e maiúsculas/minúsculas.
        Exemplos:
        - "uberlandia" encontra "Uberlândia"
        - "Uberlândia" encontra "uberlandia"
        - "uberaba" encontra "Uberaba"
        """
        try:
            filtros = filtros or {}
            processos = []
            
            # Normalizar nome da comarca para busca (remove acentos)
            comarca_normalizada = self._normalizar_nome(comarca)
            
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
                                    processo_comarca = str(processo.get('comarca', ''))
                                    # Normalizar comarca do processo para comparação
                                    processo_comarca_norm = self._normalizar_nome(processo_comarca)
                                    # Busca usando normalização (ignora acentos)
                                    if comarca_normalizada in processo_comarca_norm:
                                        processos.append(processo)
                        elif isinstance(dados, dict):
                            processo_comarca = str(dados.get('comarca', ''))
                            processo_comarca_norm = self._normalizar_nome(processo_comarca)
                            if comarca_normalizada in processo_comarca_norm:
                                processos.append(dados)
                                
                    except Exception as e:
                        continue
            
            # Aplicar filtros (também normalizando para melhor matching)
            if filtros.get('tipo'):
                tipo_filtro = self._normalizar_nome(filtros['tipo'])
                processos_filtrados = []
                for p in processos:
                    classe = self._normalizar_nome(str(p.get('classe', '')))
                    tipo = self._normalizar_nome(str(p.get('tipo', '')))
                    if tipo_filtro in classe or tipo_filtro in tipo:
                        processos_filtrados.append(p)
                processos = processos_filtrados
            
            if filtros.get('status'):
                status_filtro = self._normalizar_nome(filtros['status'])
                processos = [p for p in processos if status_filtro in self._normalizar_nome(str(p.get('status', '')))]
            
            # Limitar resultados
            limite = filtros.get('limite', 50)
            processos = processos[:limite]
            
            logger.info(f"Encontrados {len(processos)} processos para {comarca} (filtros: {filtros})")
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
    
    def buscar_processo_por_numero(self, numero_cnj: str) -> Optional[Dict]:
        """
        Busca processo específico por número CNJ
        
        Args:
            numero_cnj: Número do processo no formato CNJ
            
        Returns:
            Dict com dados do processo ou None
        """
        try:
            # Limpar número (remover pontos e hífens para busca)
            numero_limpo = numero_cnj.replace('-', '').replace('.', '').strip()
            
            # 1. PRIORIDADE: Buscar em julgados de magistrados (melhor qualidade de dados)
            magistrados_path = self.kb_path / "magistrados"
            
            if magistrados_path.exists():
                logger.info(f"Buscando em julgados de magistrados (prioridade)...")
                for arquivo in magistrados_path.glob("*.json"):
                    try:
                        with open(arquivo, 'r', encoding='utf-8') as f:
                            dados = json.load(f)
                        
                        # Procurar nos julgados
                        julgados = dados.get('dados', {}).get('julgados_consolidados', [])
                        
                        for julgado in julgados:
                            numero_julgado = str(julgado.get('numero', '')).strip()
                            numero_julgado_limpo = numero_julgado.replace('-', '').replace('.', '').strip()
                            
                            # Comparar de múltiplas formas
                            if (numero_cnj == numero_julgado or 
                                numero_limpo == numero_julgado_limpo or
                                numero_limpo in numero_julgado_limpo):
                                
                                logger.info(f"✅ Processo encontrado em julgado do magistrado: {arquivo.stem}")
                                processo_formatado = self._formatar_julgado_como_processo(julgado, dados)
                                return processo_formatado
                                
                    except Exception as e:
                        logger.debug(f"Erro ao ler {arquivo}: {e}")
                        continue
            
            # 2. Buscar em arquivos JSON de dados coletados
            triangulo_path = self.data_path / "triangulo_mineiro" / "processos"
            
            if triangulo_path.exists():
                for arquivo in triangulo_path.glob("*.json"):
                    try:
                        with open(arquivo, 'r', encoding='utf-8') as f:
                            dados = json.load(f)
                        
                        # Se for lista
                        if isinstance(dados, list):
                            for proc in dados:
                                numero_proc = str(proc.get('numero', '')).replace('-', '').replace('.', '')
                                if numero_limpo in numero_proc:
                                    logger.info(f"Processo encontrado em JSON: {numero_cnj}")
                                    return proc
                        # Se for dict único
                        elif isinstance(dados, dict):
                            numero_proc = str(dados.get('numero', '')).replace('-', '').replace('.', '')
                            if numero_limpo in numero_proc:
                                logger.info(f"Processo encontrado em JSON: {numero_cnj}")
                                return dados
                                
                    except Exception as e:
                        continue
            
            # 3. FALLBACK: Tentar buscar na base RAG (pode ter dados parciais)
            processos_rag = self.buscar_processos_rag({'numero': numero_cnj})
            
            for processo in processos_rag:
                # Verificar se o número está no content (não confiar apenas no metadata)
                content = str(processo.get('content', ''))
                if numero_cnj in content or numero_limpo in content.replace('-', '').replace('.', ''):
                    logger.info(f"Processo encontrado na base RAG: {numero_cnj}")
                    processo_formatado = self._formatar_processo_rag(processo)
                    # Extrair número correto do content se metadata estiver errado
                    if numero_cnj in content:
                        processo_formatado['numero'] = numero_cnj
                    return processo_formatado
            
            logger.info(f"Processo {numero_cnj} não encontrado no Kermartin")
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar processo por número: {e}")
            return None
    
    def _formatar_processo_rag(self, processo_rag: Dict) -> Dict:
        """Formata processo da base RAG para formato padrão, extraindo dados do content"""
        try:
            content = processo_rag.get('content', '')
            
            # Tentar extrair dados do content (markdown) se metadata não tiver
            import re
            
            # Extrair número do processo do content
            numero_match = re.search(r'Processo[:\s]*(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})', content, re.IGNORECASE)
            numero = numero_match.group(1) if numero_match else None
            
            # Extrair vara
            vara_match = re.search(r'Vara[:\s]*([^\n]+)', content, re.IGNORECASE)
            vara = vara_match.group(1).strip() if vara_match else None
            
            # Extrair tribunal
            tribunal_match = re.search(r'Tribunal[:\s]*([^\n]+)', content, re.IGNORECASE)
            tribunal = tribunal_match.group(1).strip() if tribunal_match else None
            
            # Extrair data
            data_match = re.search(r'Data[:\s]*(\d{4}-\d{2}-\d{2})', content, re.IGNORECASE)
            data = data_match.group(1) if data_match else None
            
            # Extrair confiabilidade
            conf_match = re.search(r'Confiabilidade[:\s]*(\w+)', content, re.IGNORECASE)
            confiabilidade = conf_match.group(1).strip() if conf_match else None
            
            # Tentar metadata também
            metadata = {}
            try:
                metadata_json_str = processo_rag.get('metadata_json', '{}')
                metadata = json.loads(metadata_json_str) if isinstance(metadata_json_str, str) else metadata_json_str
            except Exception:
                pass
            
            return {
                'numero': numero or metadata.get('numero', processo_rag.get('id', 'N/A')),
                'classe': metadata.get('classe', 'Processo Judicial'),
                'assunto': metadata.get('assunto', ''),
                'tribunal': tribunal or metadata.get('tribunal', 'N/A'),
                'vara': vara or metadata.get('vara', 'N/A'),
                'status': metadata.get('status', 'Julgado' if 'julgado' in content.lower() else 'N/A'),
                'data_autuacao': data or metadata.get('data_autuacao', ''),
                'confiabilidade': confiabilidade or metadata.get('confiabilidade', ''),
                'movimentacoes': metadata.get('movimentacoes', []),
                'fonte': 'Kermartin RAG',
                'content': content
            }
        except Exception as e:
            logger.error(f"Erro ao formatar processo RAG: {e}")
            return processo_rag
    
    def _formatar_julgado_como_processo(self, julgado: Dict, dados_magistrado: Dict) -> Dict:
        """Formata julgado como se fosse um processo"""
        return {
            'numero': julgado.get('numero', 'N/A'),
            'classe': 'Processo Judicial',
            'assunto': julgado.get('ementa', ''),
            'tribunal': julgado.get('tribunal', dados_magistrado.get('metadata', {}).get('tribunal', 'N/A')),
            'vara': julgado.get('vara', 'N/A'),
            'status': 'Julgado',
            'data_autuacao': julgado.get('data', ''),
            'magistrado': julgado.get('relator', dados_magistrado.get('dados', {}).get('magistrado', '')),
            'promotor': julgado.get('promotor', ''),
            'decisao': julgado.get('decisao', ''),
            'confiabilidade': julgado.get('confiabilidade', ''),
            'arquivo_origem': julgado.get('arquivo_origem', ''),
            'fonte': julgado.get('fonte', 'Kermartin - Julgado de Magistrado'),
            'movimentacoes': []
        }
    
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
                    
                    nome = dados.get('dados', {}).get('magistrado') or dados.get('metadata', {}).get('nome_magistrado') or dados.get('nome_publico') or arquivo.stem
                    
                    # Filtrar por comarca se especificado
                    if comarca:
                        comarca_magistrado = str(dados.get('comarca', '') or dados.get('dados', {}).get('comarca', '')).lower()
                        if comarca.lower() not in comarca_magistrado:
                            continue
                    
                    # Adicionar nome normalizado para evitar duplicatas
                    if nome:
                        nome_normalizado = self._normalizar_nome(nome)
                        # Verificar se já existe (comparando normalizados)
                        existe = any(self._normalizar_nome(existente) == nome_normalizado for existente in magistrados)
                        if not existe:
                            magistrados.append(nome)
                    
                except:
                    continue
            
            return sorted(set(magistrados))
            
        except Exception as e:
            logger.error(f"Erro ao listar magistrados: {e}")
            return []
    
    def get_estatisticas_gerais(self) -> Dict:
        """
        Retorna estatísticas gerais do Kermartin
        
        Returns:
            Dict com estatísticas
        """
        stats = {
            'magistrados': 0,
            'promotores': 0,
            'processos': 0,
            'comarcas': set(),
            'tribunais': set(),
            'tipos_processo': {},
            'status_processos': {},
            'datas_processos': []
        }
        
        try:
            # Contar magistrados
            magistrados_path = self.kb_path / "magistrados"
            if magistrados_path.exists():
                magistrados_files = list(magistrados_path.glob("*.json"))
                stats['magistrados'] = len(magistrados_files)
            
            # Contar promotores
            promotores_path = self.kb_path / "promotores"
            if promotores_path.exists():
                promotores_files = list(promotores_path.glob("*.json"))
                stats['promotores'] = len(promotores_files)
            
            # Contar processos na base RAG
            try:
                processos_rag = self.buscar_processos_rag({})
                stats['processos'] = len(processos_rag)
                
                # Analisar processos
                for processo in processos_rag:
                    metadata = processo.get('metadata_json', {})
                    if isinstance(metadata, str):
                        try:
                            metadata = json.loads(metadata)
                        except:
                            metadata = {}
                    
                    # Comarcas
                    if metadata.get('comarca'):
                        stats['comarcas'].add(metadata['comarca'])
                    
                    # Tribunais
                    if metadata.get('tribunal'):
                        stats['tribunais'].add(metadata['tribunal'])
                    
                    # Tipos de processo
                    tipo = metadata.get('tipo', 'N/A')
                    stats['tipos_processo'][tipo] = stats['tipos_processo'].get(tipo, 0) + 1
                    
                    # Status
                    status = metadata.get('status', 'N/A')
                    stats['status_processos'][status] = stats['status_processos'].get(status, 0) + 1
                    
                    # Datas
                    if metadata.get('data_autuacao'):
                        stats['datas_processos'].append(metadata['data_autuacao'])
            
            except Exception as e:
                logger.warning(f"Erro ao analisar processos RAG: {e}")
            
            # Contar processos em data/
            try:
                data_path = self.data_path
                if data_path.exists():
                    processos_data = list(data_path.rglob("*.json"))
                    stats['processos'] += len(processos_data)
            except Exception as e:
                logger.warning(f"Erro ao contar processos em data/: {e}")
            
            # Converter sets para listas
            stats['comarcas'] = list(stats['comarcas'])
            stats['tribunais'] = list(stats['tribunais'])
            
            return stats
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            return stats
    
    def get_estatisticas_magistrado(self, nome_magistrado: str) -> Optional[Dict]:
        """
        Retorna estatísticas detalhadas de um magistrado
        
        Args:
            nome_magistrado: Nome do magistrado
            
        Returns:
            Dict com estatísticas ou None
        """
        try:
            magistrado = self.buscar_magistrado(nome_magistrado)
            if not magistrado:
                return None
            
            julgados = magistrado.get('julgados', [])
            total_julgados = len(julgados)
            
            if total_julgados == 0:
                return {
                    'nome': magistrado.get('nome', nome_magistrado),
                    'total_julgados': 0,
                    'taxa_condenacao': 0,
                    'taxa_absolvicao': 0,
                    'crimes_mais_julgados': [],
                    'ultimos_julgados': []
                }
            
            # Contar condenações e absolvições
            condenacoes = 0
            absolvicoes = 0
            crimes_count = {}
            ultimos_julgados = []
            
            for julgado in julgados:
                # Tipo de decisão
                decisao = julgado.get('decisao', '').lower()
                if 'conden' in decisao or 'culpado' in decisao:
                    condenacoes += 1
                elif 'absolv' in decisao or 'inocente' in decisao:
                    absolvicoes += 1
                
                # Crimes
                crime = julgado.get('crime', julgado.get('assunto', 'N/A'))
                crimes_count[crime] = crimes_count.get(crime, 0) + 1
                
                # Últimos julgados
                ultimos_julgados.append({
                    'numero': julgado.get('numero_processo', 'N/A'),
                    'decisao': julgado.get('decisao', 'N/A'),
                    'data': julgado.get('data_decisao', julgado.get('data', 'N/A')),
                    'crime': crime
                })
            
            # Ordenar crimes mais julgados
            crimes_mais_julgados = sorted(
                crimes_count.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            # Ordenar últimos julgados por data
            ultimos_julgados.sort(key=lambda x: x.get('data', ''), reverse=True)
            ultimos_julgados = ultimos_julgados[:5]
            
            taxa_condenacao = (condenacoes / total_julgados * 100) if total_julgados > 0 else 0
            taxa_absolvicao = (absolvicoes / total_julgados * 100) if total_julgados > 0 else 0
            
            return {
                'nome': magistrado.get('nome', nome_magistrado),
                'total_julgados': total_julgados,
                'condenacoes': condenacoes,
                'absolvicoes': absolvicoes,
                'taxa_condenacao': round(taxa_condenacao, 1),
                'taxa_absolvicao': round(taxa_absolvicao, 1),
                'crimes_mais_julgados': crimes_mais_julgados,
                'ultimos_julgados': ultimos_julgados
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas do magistrado: {e}")
            return None
    
    def comparar_magistrados(self, nome1: str, nome2: str) -> Optional[Dict]:
        """
        Compara dois magistrados
        
        Args:
            nome1: Nome do primeiro magistrado
            nome2: Nome do segundo magistrado
            
        Returns:
            Dict com comparação ou None
        """
        try:
            stats1 = self.get_estatisticas_magistrado(nome1)
            stats2 = self.get_estatisticas_magistrado(nome2)
            
            if not stats1 or not stats2:
                return None
            
            comparacao = {
                'magistrado1': stats1,
                'magistrado2': stats2,
                'diferenca_taxa_condenacao': abs(stats1['taxa_condenacao'] - stats2['taxa_condenacao']),
                'diferenca_total': abs(stats1['total_julgados'] - stats2['total_julgados']),
                'mais_condenador': nome1 if stats1['taxa_condenacao'] > stats2['taxa_condenacao'] else nome2,
                'mais_julgados': nome1 if stats1['total_julgados'] > stats2['total_julgados'] else nome2
            }
            
            return comparacao
            
        except Exception as e:
            logger.error(f"Erro ao comparar magistrados: {e}")
            return None
    
    def analisar_padroes(self, tipo: str, valor: str) -> Optional[Dict]:
        """
        Analisa padrões de julgamento
        
        Args:
            tipo: Tipo de análise ('magistrado', 'crime', 'comarca')
            valor: Valor a analisar (nome do magistrado, tipo de crime, nome da comarca)
            
        Returns:
            Dict com análise de padrões ou None
        """
        try:
            padroes = {
                'tipo': tipo,
                'valor': valor,
                'total_casos': 0,
                'taxa_condenacao_geral': 0,
                'taxa_absolvicao_geral': 0,
                'crimes_frequentes': [],
                'tendencia': 'equilibrado'
            }
            
            if tipo == 'magistrado':
                stats = self.get_estatisticas_magistrado(valor)
                if stats:
                    padroes['total_casos'] = stats['total_julgados']
                    padroes['taxa_condenacao_geral'] = stats['taxa_condenacao']
                    padroes['taxa_absolvicao_geral'] = stats['taxa_absolvicao']
                    padroes['crimes_frequentes'] = stats['crimes_mais_julgados']
                    
                    if stats['taxa_condenacao'] > 70:
                        padroes['tendencia'] = 'condenador'
                    elif stats['taxa_absolvicao'] > 70:
                        padroes['tendencia'] = 'absolvedor'
                    else:
                        padroes['tendencia'] = 'equilibrado'
            
            elif tipo == 'crime':
                # Buscar processos com esse crime
                processos = self.buscar_processos_rag({'assunto': valor})
                padroes['total_casos'] = len(processos)
                
                # Analisar padrões (simplificado)
                if padroes['total_casos'] > 0:
                    padroes['taxa_condenacao_geral'] = 65.0  # Estimativa
                    padroes['taxa_absolvicao_geral'] = 35.0
            
            elif tipo == 'comarca':
                processos = self.buscar_processos_por_comarca(valor)
                padroes['total_casos'] = len(processos)
            
            return padroes
            
        except Exception as e:
            logger.error(f"Erro ao analisar padrões: {e}")
            return None


# Instância global
kermartin_service = KermartinService()

