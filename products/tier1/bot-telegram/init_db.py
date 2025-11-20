#!/usr/bin/env python3
"""
Script para inicializar o banco de dados
Cria todas as tabelas necessárias para o bot Telegram
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar .env do diretório pai
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"📝 Carregando .env de: {env_path}")
else:
    print(f"⚠️  .env não encontrado em: {env_path}")
    print("   Usando variáveis de ambiente do sistema")

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Importar modelos para garantir que Base tenha todas as tabelas
from shared.database.models import (
    User, Chat, Prazo, Notificacao, Alerta, ConsultaJurisprudencia
)

# Importar função de inicialização
from shared.config.database import init_db, engine

print("=" * 60)
print("🗄️  INICIALIZAÇÃO DO BANCO DE DADOS")
print("=" * 60)
print()

try:
    # Criar todas as tabelas
    print("📋 Criando tabelas...")
    init_db()
    
    print("✅ Tabelas criadas com sucesso!")
    print()
    
    # Verificar tabelas criadas
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print(f"📊 Tabelas criadas ({len(tables)}):")
    for table in sorted(tables):
        print(f"   ✅ {table}")
    
    print()
    print("=" * 60)
    print("✅ BANCO DE DADOS INICIALIZADO COM SUCESSO!")
    print("=" * 60)
    print()
    print("🚀 Agora você pode reiniciar o bot e ele usará o banco!")
    
except Exception as e:
    print("❌ ERRO ao inicializar banco de dados!")
    print(f"   {str(e)}")
    print()
    print("🔧 Verifique:")
    print("   1. PostgreSQL está rodando: sudo systemctl status postgresql")
    print("   2. .env está configurado corretamente")
    print("   3. Usuário e senha estão corretos")
    sys.exit(1)

