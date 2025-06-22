# test_integration.py
# Este script verifica se a aplicação consegue se comunicar corretamente
# com o banco de dados PostgreSQL. Ele testa a configuração do .env,
# a conexão e as operações básicas de leitura de dados.

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_project_dependencies():
    """Verifica se as bibliotecas essenciais estão instaladas."""
    print("=== Teste 1: Verificação de Dependências ===")
    try:
        import psycopg2
        print("✓ Biblioteca 'psycopg2' encontrada.")
        from dotenv import load_dotenv
        print("✓ Biblioteca 'python-dotenv' encontrada.")
        return True
    except ImportError as e:
        print(f"✗ Dependência não encontrada: {e}.")
        print("   Execute: pip install psycopg2-binary python-dotenv")
        return False

def test_env_file_configuration():
    """Verifica se o arquivo .env existe e contém a variável necessária."""
    print("\n=== Teste 2: Configuração do Ambiente (.env) ===")
    if not os.path.exists('.env'):
        print("✗ Arquivo .env não encontrado.")
        print("   É necessário criar um arquivo .env com a variável DATABASE_URL.")
        return False
    print("✓ Arquivo .env encontrado.")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("✗ Variável DATABASE_URL não foi encontrada dentro do arquivo .env.")
        return False
    
    if 'user' in database_url and 'password' in database_url and 'host' in database_url:
        # Checagem simples para ver se a URL não está com os placeholders
        if '[user]' in database_url or '[password]' in database_url:
             print("⚠️  Aviso: DATABASE_URL parece conter placeholders. Verifique se as credenciais estão corretas.")
    
    print("✓ Variável DATABASE_URL encontrada e carregada.")
    return True

def test_database_connection_and_tables():
    """Testa a conexão com o banco e verifica a existência das tabelas."""
    print("\n=== Teste 3: Conexão com o Banco e Estrutura das Tabelas ===")
    try:
        from database import db_manager
        
        # Tenta obter uma conexão, o que força a inicialização do pool e a criação das tabelas
        conn = db_manager.get_connection()
        print("✓ Conexão com o banco de dados estabelecida com sucesso.")
        
        # Verifica se as tabelas foram criadas
        with conn.cursor() as cur:
            cur.execute("SELECT to_regclass('public.usuarios'), to_regclass('public.contatos');")
            usuarios_exists, contatos_exists = cur.fetchone()
            
            if usuarios_exists:
                print("✓ Tabela 'usuarios' existe no banco de dados.")
            else:
                print("✗ Tabela 'usuarios' não foi encontrada.")
                return False

            if contatos_exists:
                print("✓ Tabela 'contatos' existe no banco de dados.")
            else:
                print("✗ Tabela 'contatos' não foi encontrada.")
                return False
        
        db_manager.return_connection(conn)
        return True
    except Exception as e:
        print(f"✗ Falha ao conectar ou verificar tabelas: {e}")
        return False

def test_crud_read_operations():
    """Testa se as operações de leitura (obter, buscar) funcionam sem erros."""
    print("\n=== Teste 4: Operações de Leitura (CRUD) ===")
    try:
        import crud_contatos
        
        # A função deve retornar uma lista, mesmo que vazia, sem levantar exceções.
        contatos = crud_contatos.obter_contatos()
        print(f"✓ Função 'obter_contatos' executada. {len(contatos)} contatos retornados.")
        
        # A busca também deve funcionar sem erros.
        resultados = crud_contatos.buscar_contatos('nonexistent_test_key')
        print(f"✓ Função 'buscar_contatos' executada. {len(resultados)} resultados retornados.")
        
        return True
    except Exception as e:
        print(f"✗ Erro ao testar operações de leitura do CRUD: {e}")
        return False

def main():
    """Executa todos os testes de integração."""
    tests = [
        test_project_dependencies,
        test_env_file_configuration,
        test_database_connection_and_tables,
        test_crud_read_operations
    ]
    
    passed_count = sum(1 for test in tests if test())
    total_tests = len(tests)
    
    print("\n" + "="*50)
    print("RESUMO DOS TESTES DE INTEGRAÇÃO")
    print("="*50)
    print(f"Resultado: {passed_count}/{total_tests} testes passaram.")
    
    if passed_count == total_tests:
        print("\n🎉 Status: Ótimo! A aplicação está pronta para se conectar ao banco de dados.")
        return 0
    else:
        print("\n⚠️ Status: Problemas de integração detectados. Verifique os erros acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
