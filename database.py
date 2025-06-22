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
        # A inicialização é chamada externamente para melhor controle de erros
    
    def init_connection_pool(self):
        """Inicializa o pool de conexões."""
        if self.connection_pool:
            return
        try:
            connection_string = os.getenv('DATABASE_URL')
            if not connection_string:
                raise ValueError("DATABASE_URL não encontrada no arquivo .env")
            
            # Cria um pool simples de conexões
            self.connection_pool = pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=connection_string
            )
            print("Pool de conexões com PostgreSQL criado com sucesso.")
            self._create_tables()
            
        except (psycopg2.OperationalError, ValueError) as e:
            print(f"Erro ao inicializar pool de conexões: {e}")
            self.connection_pool = None # Garante que o pool não seja usado se falhar
            raise # Repassa a exceção para ser tratada na GUI

    def get_connection(self):
        """Obtém uma conexão do pool. Inicializa o pool se necessário."""
        if not self.connection_pool:
            self.init_connection_pool()
        
        if self.connection_pool:
            return self.connection_pool.getconn()
        
        # Se ainda assim o pool for None, lança um erro
        raise Exception("Pool de conexões não está disponível.")

    def return_connection(self, conn):
        """Devolve uma conexão ao pool."""
        if self.connection_pool and conn:
            self.connection_pool.putconn(conn)
    
    def _create_tables(self):
        """
        Método privado para criar as tabelas `usuarios` e `contatos`
        se elas ainda não existirem no banco de dados.
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                # Tabela de usuários para o sistema de login
                cur.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    email VARCHAR(120),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP WITH TIME ZONE
                );
                """)
                
                # Tabela de contatos
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
                print("Tabelas 'usuarios' e 'contatos' verificadas/criadas.")
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")
            conn.rollback()
        finally:
            self.return_connection(conn)
    
    def close_all_connections(self):
        """Fecha todas as conexões do pool. Chamado ao sair da aplicação."""
        if self.connection_pool:
            self.connection_pool.closeall()
            print("Todas as conexões com o banco foram fechadas.")

# Instância global para ser usada em toda a aplicação
db_manager = DatabaseManager()
