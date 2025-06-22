# test_auth.py
# Este script executa uma bateria de testes para validar todo o sistema
# de autenticação, desde o registro e hashing de senha até o login e logout.

import os
import sys

# Função para garantir que o diretório do projeto esteja no path do Python
# para que os outros módulos possam ser importados.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_imports_and_db_connection():
    """Testa se as dependências e a conexão com o banco funcionam."""
    print("=== Teste 1: Importações e Conexão com o Banco ===")
    try:
        import bcrypt
        print("✓ Biblioteca 'bcrypt' importada com sucesso.")
        from database import db_manager
        print("✓ Módulo 'database' importado com sucesso.")
        from auth import auth_manager
        print("✓ Módulo 'auth' importado com sucesso.")
        
        # Força a inicialização da conexão para validar as credenciais do .env
        conn = db_manager.get_connection()
        db_manager.return_connection(conn)
        print("✓ Conexão com o banco de dados PostgreSQL bem-sucedida.")
        return True
    except Exception as e:
        print(f"✗ Falha crítica: {e}")
        print("   Verifique se as dependências (pip install bcrypt psycopg2-binary python-dotenv) estão instaladas e se o arquivo .env está correto.")
        return False

def test_password_hashing():
    """Testa se a criação de hash e a verificação de senha estão corretas."""
    print("\n=== Teste 2: Criptografia de Senha (Hashing) ===")
    try:
        from auth import auth_manager
        password = "senha_super_secreta_123"
        hashed_password = auth_manager._hash_password(password)
        
        if not isinstance(hashed_password, bytes):
            print("✗ Falha: O hash da senha não foi gerado corretamente.")
            return False
        print("✓ Geração de hash funcionando.")

        if not auth_manager._verify_password(password, hashed_password.decode('utf-8')):
            print("✗ Falha: A verificação da senha correta falhou.")
            return False
        print("✓ Verificação de senha correta funcionando.")

        if auth_manager._verify_password("senha_errada", hashed_password.decode('utf-8')):
            print("✗ Falha: A verificação de senha incorreta retornou 'True'.")
            return False
        print("✓ Verificação de senha incorreta funcionando.")
        
        return True
    except Exception as e:
        print(f"✗ Erro inesperado no teste de hashing: {e}")
        return False

def test_user_lifecycle():
    """Testa o ciclo de vida completo de um usuário: registro, login, falhas e limpeza."""
    print("\n=== Teste 3: Ciclo de Vida do Usuário (Registro e Login) ===")
    try:
        from auth import auth_manager
        from database import db_manager

        # Dados do usuário de teste
        test_username = "tester_12345"
        test_password = "password123"
        
        # --- Limpeza Pré-teste ---
        # Garante que o usuário de teste não exista antes de começar.
        conn = db_manager.get_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM usuarios WHERE username = %s", (test_username,))
        conn.commit()
        db_manager.return_connection(conn)
        print("✓ Limpeza de usuário de teste pré-execução realizada.")
        
        # --- Teste de Registro ---
        success, msg = auth_manager.register_user(test_username, test_password, "tester@email.com")
        if not success:
            print(f"✗ Falha ao registrar usuário válido: {msg}")
            return False
        print("✓ Registro de usuário válido bem-sucedido.")
        
        # --- Teste de Registro Duplicado ---
        success, msg = auth_manager.register_user(test_username, test_password)
        if success:
            print("✗ Falha: Sistema permitiu registro de usuário duplicado.")
            return False
        print("✓ Prevenção de registro duplicado funcionando.")

        # --- Teste de Login Válido ---
        success, msg = auth_manager.login_user(test_username, test_password)
        if not success:
            print(f"✗ Falha no login com credenciais válidas: {msg}")
            return False
        print("✓ Login com credenciais válidas bem-sucedido.")

        # --- Teste de Verificação de Sessão ---
        if not auth_manager.is_logged_in() or auth_manager.get_current_user()['username'] != test_username:
            print("✗ Falha ao verificar que o usuário está logado.")
            return False
        print("✓ Gerenciamento de sessão (is_logged_in) funcionando.")

        # --- Teste de Logout ---
        auth_manager.logout_user()
        if auth_manager.is_logged_in():
            print("✗ Falha: Usuário continua logado após o logout.")
            return False
        print("✓ Logout bem-sucedido.")

        # --- Teste de Login com Senha Errada ---
        success, msg = auth_manager.login_user(test_username, "senhaerrada")
        if success:
            print("✗ Falha: Sistema permitiu login com senha incorreta.")
            return False
        print("✓ Bloqueio de login com senha incorreta funcionando.")

        return True
    except Exception as e:
        print(f"✗ Erro inesperado no ciclo de vida do usuário: {e}")
        return False
    finally:
        # --- Limpeza Pós-teste ---
        try:
            conn = db_manager.get_connection()
            with conn.cursor() as cur:
                cur.execute("DELETE FROM usuarios WHERE username = %s", (test_username,))
            conn.commit()
            db_manager.return_connection(conn)
            print("✓ Limpeza de usuário de teste pós-execução realizada.")
        except Exception as e:
            print(f"AVISO: Falha ao limpar usuário de teste: {e}")

def main():
    """Executa todos os testes em sequência."""
    tests = [
        test_imports_and_db_connection,
        test_password_hashing,
        test_user_lifecycle,
    ]
    
    passed_count = 0
    for test_func in tests:
        if test_func():
            passed_count += 1
    
    print("\n" + "="*50)
    print("RESUMO DOS TESTES DE AUTENTICAÇÃO")
    print("="*50)
    print(f"Total de testes executados: {len(tests)}")
    print(f"Testes que passaram: {passed_count}")
    print(f"Testes que falharam: {len(tests) - passed_count}")
    print("="*50)
    
    if passed_count == len(tests):
        print("\n🎉 Status: Excelente! O sistema de autenticação está robusto e seguro.")
        return 0  # Código de saída 0 indica sucesso
    else:
        print("\n⚠️ Status: Atenção! Foram encontrados problemas. Revise os logs acima.")
        return 1  # Código de saída 1 indica falha

if __name__ == "__main__":
    sys.exit(main())
