#!/usr/bin/env python3
"""
Teste de conexão com PostgreSQL para o bot Telegram
"""

import sys
import os

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Carregar .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

DATABASE_URL = os.getenv('DATABASE_URL')

print("=" * 60)
print("🧪 TESTE DE CONEXÃO - BOT TELEGRAM")
print("=" * 60)
print()

print(f"📍 Database URL: {DATABASE_URL}")
print()

try:
    # Criar engine
    engine = create_engine(DATABASE_URL)
    
    # Testar conexão
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        
        print("✅ Conexão estabelecida com sucesso!")
        print(f"📊 PostgreSQL: {version[:50]}...")
        print()
        
        # Verificar banco de dados
        result = conn.execute(text("SELECT current_database();"))
        db_name = result.fetchone()[0]
        print(f"🗄️  Banco de dados: {db_name}")
        
        # Listar tabelas
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """))
        tables = result.fetchall()
        
        if tables:
            print(f"\n📋 Tabelas encontradas ({len(tables)}):")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("\n⚠️  Nenhuma tabela encontrada (banco vazio)")
            print("   Execute as migrations: alembic upgrade head")
        
        print()
        print("=" * 60)
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        
except Exception as e:
    print("❌ ERRO DE CONEXÃO!")
    print(f"   {str(e)}")
    print()
    print("🔧 Solução:")
    print("   1. Verifique se PostgreSQL está rodando:")
    print("      sudo systemctl status postgresql")
    print()
    print("   2. Verifique o .env:")
    print("      cat ../.env | grep DATABASE_URL")
    print()
    print("   3. Teste a senha manualmente:")
    print("      psql -U genesys -d genesys_db -h localhost")
    print()
    sys.exit(1)

