# database.py
# Versão simplificada que usa um banco de dados local SQLite.
# Não precisa de internet, .env ou senhas. Funciona em qualquer máquina.

import sqlite3

DB_FILE = "agenda.db"

def get_db_connection():
    """Cria e retorna uma conexão com o arquivo de banco de dados local."""
    conn = sqlite3.connect(DB_FILE)
    # Permite acessar colunas pelo nome, como um dicionário.
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """
    Inicializa o banco de dados, criando as tabelas 'usuarios' e 'contatos'
    se elas ainda não existirem. É chamada uma vez quando o programa inicia.
    """
    print("INFO: Verificando e inicializando banco de dados local (SQLite)...")
    conn = get_db_connection()
    try:
        with conn: # 'with' gerencia o commit e rollback automaticamente
            # Tabela de usuários para o sistema de login
            conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            
            # Tabela de contatos
            conn.execute("""
            CREATE TABLE IF NOT EXISTS contatos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT UNIQUE NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            print("INFO: Banco de dados pronto para uso.")
    except Exception as e:
        print(f"ERRO_CRITICO: Não foi possível criar as tabelas: {e}")
        # Se não conseguir criar as tabelas, o programa não pode continuar.
        raise
    finally:
        conn.close()

# Instância global do gerenciador (simplificado)
# Agora só contém a função de inicialização
db_initializer = init_database
