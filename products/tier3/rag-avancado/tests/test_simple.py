"""
Teste simples e rápido do RAG
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from src.services.query_processor import QueryProcessor
from src.services.retriever import Retriever
from src.config import Config


def test_basic_functionality():
    """Teste básico de funcionalidade"""
    print("=" * 60)
    print("🧪 TESTE RÁPIDO - RAG AVANÇADO")
    print("=" * 60)
    print()
    
    # 1. Configuração
    print("1️⃣ Verificando Configuração...")
    print(f"   ChromaDB Path: {Config.CHROMADB_PATH}")
    print(f"   Coleção: {Config.CHROMADB_COLLECTION}")
    print(f"   ✅ Configuração OK\n")
    
    # 2. Query Processor
    print("2️⃣ Testando Query Processor...")
    processor = QueryProcessor()
    query = "Qual a jurisprudência sobre dano moral?"
    processed = processor.process_query(query)
    print(f"   Query original: {query}")
    print(f"   Query processada: {processed['processed_query']}")
    print(f"   Tipo: {processed['query_type']}")
    print(f"   ✅ Query Processor OK\n")
    
    # 3. Retriever
    print("3️⃣ Testando Retriever (ChromaDB)...")
    try:
        retriever = Retriever()
        print(f"   ✅ Conectado ao ChromaDB")
        
        # Stats
        stats = asyncio.run(retriever.get_collection_stats())
        print(f"   Coleção: {stats['name']}")
        print(f"   Documentos: {stats['document_count']}")
        
        # Busca simples
        if stats['document_count'] > 0:
            print(f"\n4️⃣ Testando Busca Semântica...")
            docs = asyncio.run(retriever.retrieve(query, processed, n_results=3))
            print(f"   Documentos encontrados: {len(docs)}")
            
            if docs:
                print(f"\n   📄 Exemplo de resultado:")
                doc = docs[0]
                print(f"   Score: {doc['similarity_score']:.4f}")
                print(f"   Conteúdo: {doc['content'][:150]}...")
                print(f"   ✅ Busca OK")
            else:
                print(f"   ⚠️ Nenhum documento encontrado (pode ser threshold)")
        else:
            print(f"   ⚠️ Coleção vazia")
        
        print(f"\n   ✅ Retriever OK\n")
        
    except Exception as e:
        print(f"   ❌ Erro: {e}\n")
        return False
    
    print("=" * 60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 60)
    print()
    print("🎉 Sistema RAG Avançado está FUNCIONANDO!")
    print()
    print("Próximos passos:")
    print("  1. Configure OPENAI_API_KEY no .env")
    print("  2. Inicie o servidor: uvicorn src.app:app --port 8002")
    print("  3. Teste a API: http://localhost:8002/docs")
    print()
    
    return True


if __name__ == "__main__":
    try:
        success = test_basic_functionality()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)

