# database.py
# Gerencia a conexão com o banco de dados PostgreSQL (Neon) usando um pool
# e cuida da criação inicial das tabelas.

import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class DatabaseManager:
    """Gerenciador de pool de conexões com o banco de dados PostgreSQL."""
    def __init__(self):
        self.connection_pool = None
    
    def init_connection_pool(self):
        """Inicializa o pool de conexões. Lança uma exceção detalhada em caso de falha."""
        if self.connection_pool:
            return
            
        try:
            connection_string = os.getenv('DATABASE_URL')
            if not connection_string:
                raise ValueError("Variável 'DATABASE_URL' não encontrada ou está vazia no arquivo .env.")
            
            print("INFO: Tentando criar pool de conexões com o PostgreSQL...")
            self.connection_pool = pool.SimpleConnectionPool(
                minconn=1, maxconn=10, dsn=connection_string
            )
            print("INFO: Pool de conexões criado com sucesso.")
            
            print("INFO: Verificando e criando tabelas, se necessário...")
            conn = self.get_connection()
            try:
                self._create_tables_if_not_exists(conn)
            finally:
                self.return_connection(conn)
            
        except (psycopg2.OperationalError, ValueError) as e:
            print(f"ERRO_CRITICO: Falha ao inicializar a conexão com o banco de dados: {e}")
            self.connection_pool = None
            raise 

    def get_connection(self):
        """Obtém uma conexão do pool."""
        if not self.connection_pool:
            raise Exception("O pool de conexões não foi inicializado.")
        return self.connection_pool.getconn()

    def return_connection(self, conn):
        """Devolve uma conexão ao pool."""
        if self.connection_pool and conn:
            self.connection_pool.putconn(conn)
    
    def _create_tables_if_not_exists(self, conn):
        """Cria as tabelas `usuarios` e `contatos` usando uma conexão já existente."""
        try:
            with conn.cursor() as cur:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    email VARCHAR(120),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
                """)
                
                cur.execute("""
                CREATE TABLE IF NOT EXISTS contatos (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL,
                    telefone VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(255),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
                """)
                conn.commit()
                print("INFO: Tabelas 'usuarios' e 'contatos' verificadas/criadas.")
        except Exception as e:
            print(f"ERRO: Não foi possível criar/verificar as tabelas: {e}")
            conn.rollback()
            raise
    
    def close_all_connections(self):
        """Fecha todas as conexões do pool."""
        if self.connection_pool:
            self.connection_pool.closeall()
            print("INFO: Todas as conexões com o banco foram fechadas.")

# Instância global
db_manager = DatabaseManager()
