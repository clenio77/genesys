"""
Microserviço 2: Retriever
Responsável por buscar documentos relevantes no ChromaDB
"""

from typing import Dict, List, Optional
import chromadb
from chromadb.config import Settings
from pathlib import Path

from src.config import Config


class Retriever:
    """Busca documentos relevantes no ChromaDB do Kermartin"""
    
    def __init__(self):
        self.chroma_path = Path(Config.CHROMADB_PATH)
        self.client = None
        self.collection = None
        self._initialize_chromadb()
    
    def _initialize_chromadb(self):
        """Inicializa conexão com ChromaDB"""
        try:
            # Verificar se path existe
            if not self.chroma_path.exists():
                raise ValueError(f"ChromaDB path não existe: {self.chroma_path}")
            
            # Conectar ao ChromaDB persistente
            self.client = chromadb.PersistentClient(
                path=str(self.chroma_path),
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=False
                )
            )
            
            # Obter ou criar coleção
            try:
                self.collection = self.client.get_collection(
                    name=Config.CHROMADB_COLLECTION
                )
                print(f"✅ Conectado à coleção existente: {Config.CHROMADB_COLLECTION}")
            except:
                # Se coleção não existe, criar
                self.collection = self.client.create_collection(
                    name=Config.CHROMADB_COLLECTION,
                    metadata={"hnsw:space": "cosine"}
                )
                print(f"✅ Coleção criada: {Config.CHROMADB_COLLECTION}")
        
        except Exception as e:
            print(f"❌ Erro ao inicializar ChromaDB: {e}")
            raise
    
    async def retrieve(
        self,
        query: str,
        processed_query: Dict,
        n_results: int = None
    ) -> List[Dict]:
        """
        Busca documentos relevantes
        
        Args:
            query: Query original
            processed_query: Query processada com metadata
            n_results: Número de resultados (default: TOP_K_RESULTS)
            
        Returns:
            Lista de documentos com scores de relevância
        """
        if n_results is None:
            n_results = Config.TOP_K_RESULTS
        
        try:
            # Usar query expandida para melhor recall
            search_query = processed_query.get("expanded_query", query)
            
            # Construir filtro baseado em entidades
            where_filter = self._build_filter(processed_query.get("entities", {}))
            
            # Buscar no ChromaDB
            results = self.collection.query(
                query_texts=[search_query],
                n_results=n_results * 2,  # Buscar mais para filtrar depois
                where=where_filter if where_filter else None,
                include=["documents", "metadatas", "distances"]
            )
            
            # Processar resultados
            documents = self._process_results(results, n_results)
            
            return documents
        
        except Exception as e:
            print(f"❌ Erro ao buscar documentos: {e}")
            return []
    
    def _build_filter(self, entities: Dict) -> Optional[Dict]:
        """Constrói filtro ChromaDB baseado em entidades"""
        filters = []
        
        # Filtrar por tribunal
        if tribunal := entities.get("tribunal"):
            filters.append({"tribunal": {"$eq": tribunal}})
        
        # Filtrar por magistrado (usando $eq para match exato)
        if magistrado := entities.get("magistrado"):
            filters.append({"magistrado": {"$eq": magistrado}})
        
        # Filtrar por temas (usando $eq para match exato)
        if temas := entities.get("temas"):
            # OR entre temas (apenas se houver múltiplos temas)
            tema_filters = [{"assunto": {"$eq": tema}} for tema in temas]
            if len(tema_filters) > 1:
                filters.append({"$or": tema_filters})
            elif len(tema_filters) == 1:
                filters.append(tema_filters[0])
        
        # Combinar filtros com AND
        if filters:
            if len(filters) == 1:
                return filters[0]
            else:
                return {"$and": filters}
        
        return None
    
    def _process_results(self, results: Dict, n_results: int) -> List[Dict]:
        """Processa resultados do ChromaDB"""
        documents = []
        
        # ChromaDB retorna listas paralelas
        ids = results.get("ids", [[]])[0]
        docs = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]
        
        for i, (doc_id, doc, metadata, distance) in enumerate(zip(
            ids, docs, metadatas, distances
        )):
            # Converter distance para similarity score (cosine)
            # Distance no ChromaDB: menor = mais similar
            # Similarity: 0 a 1, maior = mais similar
            similarity = 1 - distance
            
            # Filtrar por threshold
            if similarity < Config.SIMILARITY_THRESHOLD:
                continue
            
            documents.append({
                "id": doc_id,
                "content": doc,
                "metadata": metadata or {},
                "similarity_score": round(similarity, 4),
                "rank": i + 1
            })
        
        # Limitar ao número solicitado
        return documents[:n_results]
    
    async def add_document(
        self,
        document_id: str,
        content: str,
        metadata: Dict
    ) -> bool:
        """
        Adiciona documento ao ChromaDB
        
        Args:
            document_id: ID único do documento
            content: Conteúdo textual
            metadata: Metadados do documento
            
        Returns:
            True se sucesso
        """
        try:
            self.collection.add(
                ids=[document_id],
                documents=[content],
                metadatas=[metadata]
            )
            return True
        
        except Exception as e:
            print(f"❌ Erro ao adicionar documento: {e}")
            return False
    
    async def get_collection_stats(self) -> Dict:
        """Retorna estatísticas da coleção"""
        try:
            count = self.collection.count()
            
            return {
                "name": Config.CHROMADB_COLLECTION,
                "document_count": count,
                "path": str(self.chroma_path),
                "status": "connected"
            }
        
        except Exception as e:
            return {
                "name": Config.CHROMADB_COLLECTION,
                "error": str(e),
                "status": "error"
            }
    
    def list_available_collections(self) -> List[str]:
        """Lista coleções disponíveis no ChromaDB"""
        try:
            collections = self.client.list_collections()
            return [c.name for c in collections]
        except Exception as e:
            print(f"❌ Erro ao listar coleções: {e}")
            return []

