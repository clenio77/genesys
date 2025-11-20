#!/usr/bin/env python3
"""
Script helper para criar migrations Alembic
"""

import sys
import os
import subprocess
from pathlib import Path


def main():
    """Cria migration Alembic"""
    if len(sys.argv) < 2:
        print("Uso: python create_migration.py 'descrição da migration'")
        print("Exemplo: python create_migration.py 'Initial migration'")
        return 1
    
    description = sys.argv[1]
    
    # Mudar para diretório do projeto
    project_dir = Path(__file__).parent.parent
    os.chdir(project_dir)
    
    # Criar migration
    cmd = ["alembic", "revision", "--autogenerate", "-m", description]
    
    print(f"📦 Criando migration: {description}")
    print(f"💻 Comando: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        print("✅ Migration criada com sucesso!")
        print()
        print("📝 Próximo passo: Revisar a migration em alembic/versions/")
        print("💻 Aplicar migration: alembic upgrade head")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar migration: {e}")
        print(e.stderr)
        return 1


if __name__ == "__main__":
    import os
    sys.exit(main())

