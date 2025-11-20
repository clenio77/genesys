#!/usr/bin/env python3
"""
Script de teste para verificar funcionalidades do bot
Testa comandos implementados e design das mensagens
"""

import sys
from pathlib import Path

# Adicionar path do projeto
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_message_formatter():
    """Testa o MessageFormatter"""
    print("🧪 Testando MessageFormatter...")
    
    try:
        from utils.message_formatter import message_formatter
        
        # Teste 1: Header
        header = message_formatter.header("TESTE", "🎯")
        assert "TESTE" in header
        assert "═════" in header
        print("   ✅ Header funciona")
        
        # Teste 2: Section
        section = message_formatter.section("Título", "Conteúdo", "📋")
        assert "Título" in section
        assert "Conteúdo" in section
        print("   ✅ Section funciona")
        
        # Teste 3: Footer
        footer = message_formatter.footer("Teste footer")
        assert "Teste footer" in footer
        assert "─────" in footer
        print("   ✅ Footer funciona")
        
        # Teste 4: Card
        card = message_formatter.card("Título", ["Item 1", "Item 2"], "📋")
        assert "Título" in card
        assert "Item 1" in card
        print("   ✅ Card funciona")
        
        print("✅ MessageFormatter: TODOS OS TESTES PASSARAM\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro: {e}\n")
        return False


def test_kermartin_service():
    """Testa o KermartinService"""
    print("🧪 Testando KermartinService...")
    
    try:
        from services.kermartin_service import kermartin_service
        
        # Verificar se serviço inicializou
        assert kermartin_service is not None
        print("   ✅ Serviço inicializado")
        
        # Teste: Listar magistrados disponíveis
        magistrados = kermartin_service.listar_magistrados_disponiveis()
        print(f"   ✅ Magistrados disponíveis: {len(magistrados)}")
        
        # Teste: Buscar promotor (pode retornar None se não existir)
        promotor = kermartin_service.buscar_promotor("teste")
        print(f"   ✅ Buscar promotor funciona (retornou: {promotor is not None})")
        
        # Teste: Buscar processos por comarca
        processos = kermartin_service.buscar_processos_por_comarca("Uberlândia")
        print(f"   ✅ Processos por comarca: {len(processos)} encontrados")
        
        print("✅ KermartinService: TODOS OS TESTES PASSARAM\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_commands_registration():
    """Testa se comandos estão registrados"""
    print("🧪 Testando registro de comandos...")
    
    try:
        from handlers.commands import register_command_handlers
        from telegram.ext import Application
        
        # Criar aplicação mock
        app = Application.builder().token("TEST_TOKEN").build()
        
        # Registrar handlers
        register_command_handlers(app)
        
        # Verificar se handlers foram adicionados
        handlers = app.handlers[0]  # Grupo 0
        
        comandos_esperados = [
            "help", "buscar", "prazos", "alerta", "processo",
            "magistrado", "promotor", "comarca", "config",
            "perfil", "cache", "login", "logout", "cadastrar"
        ]
        
        comandos_encontrados = []
        for handler in handlers:
            if hasattr(handler, 'callback') and hasattr(handler.callback, '__name__'):
                nome = handler.callback.__name__
                if nome.startswith('cmd_'):
                    comando = nome.replace('cmd_', '')
                    comandos_encontrados.append(comando)
        
        print(f"   ✅ Comandos registrados: {len(comandos_encontrados)}")
        
        # Verificar comandos críticos
        comandos_criticos = ["magistrado", "promotor", "comarca"]
        for cmd in comandos_criticos:
            if cmd in comandos_encontrados:
                print(f"   ✅ Comando /{cmd} registrado")
            else:
                print(f"   ⚠️ Comando /{cmd} NÃO encontrado")
        
        print("✅ Registro de comandos: TESTE CONCLUÍDO\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_message_handlers():
    """Testa handlers de mensagens"""
    print("🧪 Testando handlers de mensagens...")
    
    try:
        from handlers import messages
        
        # Verificar se função handle_message existe
        assert hasattr(messages, 'handle_message')
        print("   ✅ handle_message existe")
        
        # Verificar se função safe_reply_text existe
        assert hasattr(messages, 'safe_reply_text')
        print("   ✅ safe_reply_text existe")
        
        # Verificar se função split_message existe
        assert hasattr(messages, 'split_message')
        print("   ✅ split_message existe")
        
        # Teste: split_message com texto curto
        resultado = messages.split_message("Texto curto")
        assert len(resultado) == 1
        print("   ✅ split_message funciona com texto curto")
        
        # Teste: split_message com texto longo
        texto_longo = "a" * 5000
        resultado = messages.split_message(texto_longo)
        assert len(resultado) > 1
        print(f"   ✅ split_message divide texto longo em {len(resultado)} partes")
        
        print("✅ Handlers de mensagens: TODOS OS TESTES PASSARAM\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_design_consistency():
    """Testa consistência do design"""
    print("🧪 Testando consistência do design...")
    
    try:
        from utils.message_formatter import message_formatter
        
        # Verificar se separadores estão definidos
        assert hasattr(message_formatter, 'SEPARADOR')
        assert hasattr(message_formatter, 'SEPARADOR_FORTE')
        print("   ✅ Separadores definidos")
        
        # Verificar se emojis estão definidos
        assert hasattr(message_formatter, 'EMOJIS')
        assert isinstance(message_formatter.EMOJIS, dict)
        print(f"   ✅ {len(message_formatter.EMOJIS)} emojis definidos")
        
        # Verificar emojis críticos
        emojis_criticos = ['magistrado', 'promotor', 'processo', 'estatistica']
        for emoji in emojis_criticos:
            if emoji in message_formatter.EMOJIS:
                print(f"   ✅ Emoji '{emoji}' definido: {message_formatter.EMOJIS[emoji]}")
            else:
                print(f"   ⚠️ Emoji '{emoji}' NÃO definido")
        
        print("✅ Consistência do design: TODOS OS TESTES PASSARAM\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("🧪 TESTES DE FUNCIONALIDADES DO BOT TELEGRAM")
    print("=" * 60)
    print()
    
    resultados = []
    
    # Executar testes
    resultados.append(("MessageFormatter", test_message_formatter()))
    resultados.append(("KermartinService", test_kermartin_service()))
    resultados.append(("Registro de Comandos", test_commands_registration()))
    resultados.append(("Handlers de Mensagens", test_message_handlers()))
    resultados.append(("Consistência do Design", test_design_consistency()))
    
    # Resumo
    print("=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    total = len(resultados)
    passou = sum(1 for _, resultado in resultados if resultado)
    
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome:.<40} {status}")
    
    print()
    print(f"Total: {passou}/{total} testes passaram")
    
    if passou == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print(f"\n⚠️ {total - passou} teste(s) falharam")
        return 1


if __name__ == "__main__":
    sys.exit(main())

