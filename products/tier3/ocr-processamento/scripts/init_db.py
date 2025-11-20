#!/usr/bin/env python3
"""
Script para inicializar o banco de dados
Cria todas as tabelas necessárias
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import init_db, engine
from src.models.document import Base
from sqlalchemy import inspect


def check_tables():
    """Verifica quais tabelas existem"""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    return existing_tables


def main():
    """Função principal"""
    print("=" * 60)
    print("🔧 Inicializando Banco de Dados - OCR & Processamento")
    print("=" * 60)
    print()
    
    # Verificar tabelas existentes
    existing_tables = check_tables()
    print(f"📊 Tabelas existentes: {len(existing_tables)}")
    if existing_tables:
        print("   " + ", ".join(existing_tables))
    print()
    
    # Criar tabelas
    print("📦 Criando tabelas...")
    try:
        init_db()
        print("✅ Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        return 1
    
    # Verificar tabelas criadas
    new_tables = check_tables()
    print()
    print(f"📊 Total de tabelas: {len(new_tables)}")
    print("   " + ", ".join(new_tables))
    print()
    
    print("=" * 60)
    print("✅ Banco de dados inicializado com sucesso!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

