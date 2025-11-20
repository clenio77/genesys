"""
Testes de integração com ChromaDB do Kermartin
"""

import pytest
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.retriever import Retriever
from src.services.query_processor import QueryProcessor
from src.config import Config


class TestChromaDBIntegration:
    """Testes de integração com ChromaDB"""
    
    def setup_method(self):
        """Setup antes de cada teste"""
        self.retriever = Retriever()
        self.query_processor = QueryProcessor()
    
    def test_chromadb_connection(self):
        """Testa conexão com ChromaDB"""
        assert self.retriever.client is not None, "Cliente ChromaDB não inicializado"
        assert self.retriever.collection is not None, "Coleção não encontrada"
        print(f"✅ Conectado à coleção: {Config.CHROMADB_COLLECTION}")
    
    def test_list_collections(self):
        """Lista coleções disponíveis"""
        collections = self.retriever.list_available_collections()
        assert len(collections) > 0, "Nenhuma coleção encontrada"
        print(f"✅ Coleções encontradas: {collections}")
    
    def test_get_stats(self):
        """Obtém estatísticas da coleção"""
        import asyncio
        stats = asyncio.run(self.retriever.get_collection_stats())
        
        assert stats.get("status") == "connected", "Não conectado"
        doc_count = stats.get("document_count", 0)
        print(f"✅ Documentos na coleção: {doc_count}")
        assert doc_count > 0, "Coleção vazia"
    
    def test_simple_query(self):
        """Testa consulta simples"""
        import asyncio
        
        query = "ação de indenização por dano moral"
        processed = self.query_processor.process_query(query)
        
        # Buscar documentos
        docs = asyncio.run(self.retriever.retrieve(query, processed, n_results=3))
        
        assert len(docs) > 0, "Nenhum documento encontrado"
        print(f"✅ Encontrados {len(docs)} documentos")
        
        # Verificar estrutura
        for i, doc in enumerate(docs):
            assert "id" in doc, "Documento sem ID"
            assert "content" in doc, "Documento sem conteúdo"
            assert "similarity_score" in doc, "Documento sem score"
            
            print(f"\nDoc {i+1}:")
            print(f"  ID: {doc['id']}")
            print(f"  Score: {doc['similarity_score']:.4f}")
            print(f"  Content: {doc['content'][:100]}...")
    
    def test_tribunal_filter(self):
        """Testa filtro por tribunal"""
        import asyncio
        
        query = "TJMG decisão homologação"
        processed = self.query_processor.process_query(query)
        
        # Verificar se tribunal foi extraído
        entities = processed.get("entities", {})
        if "tribunal" in entities:
            print(f"✅ Tribunal extraído: {entities['tribunal']}")
        
        docs = asyncio.run(self.retriever.retrieve(query, processed, n_results=5))
        print(f"✅ Documentos filtrados: {len(docs)}")
    
    def test_add_document(self):
        """Testa adicionar documento (apenas se permitido)"""
        import asyncio
        
        test_doc = {
            "id": "test_doc_001",
            "content": "Este é um documento de teste para validar a indexação no ChromaDB.",
            "metadata": {
                "tipo": "teste",
                "tribunal": "TEST",
                "data": "2024-10-26"
            }
        }
        
        try:
            success = asyncio.run(self.retriever.add_document(
                test_doc["id"],
                test_doc["content"],
                test_doc["metadata"]
            ))
            
            if success:
                print("✅ Documento de teste adicionado com sucesso")
            else:
                print("⚠️ Não foi possível adicionar documento de teste")
        
        except Exception as e:
            print(f"⚠️ Erro ao adicionar documento: {e}")


def run_integration_tests():
    """Executa todos os testes de integração"""
    print("=" * 60)
    print("🧪 TESTES DE INTEGRAÇÃO - CHROMADB KERMARTIN")
    print("=" * 60)
    print()
    
    tester = TestChromaDBIntegration()
    tester.setup_method()
    
    tests = [
        ("Conexão ChromaDB", tester.test_chromadb_connection),
        ("Listar Coleções", tester.test_list_collections),
        ("Estatísticas", tester.test_get_stats),
        ("Consulta Simples", tester.test_simple_query),
        ("Filtro por Tribunal", tester.test_tribunal_filter),
        ("Adicionar Documento", tester.test_add_document)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Teste: {test_name}")
        print(f"{'='*60}")
        
        try:
            test_func()
            passed += 1
            print(f"✅ {test_name} - PASSOU")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} - FALHOU: {e}")
    
    print(f"\n{'='*60}")
    print("RESUMO DOS TESTES")
    print(f"{'='*60}")
    print(f"✅ Passaram: {passed}")
    print(f"❌ Falharam: {failed}")
    print(f"Total: {len(tests)}")
    print(f"{'='*60}\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)

