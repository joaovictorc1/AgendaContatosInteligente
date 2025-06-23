# database.py
# CORREÇÃO: Adicionada a coluna 'user_id' na tabela 'contatos'
# para vincular cada contato a um usuário.

import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.connection_pool = None
    
    def init_connection_pool(self):
        if self.connection_pool:
            return
        try:
            connection_string = os.getenv('DATABASE_URL')
            if not connection_string:
                raise ValueError("Variável 'DATABASE_URL' não encontrada ou está vazia no arquivo .env.")
            
            self.connection_pool = pool.SimpleConnectionPool(
                minconn=1, maxconn=10, dsn=connection_string
            )
            
            conn = self.get_connection()
            try:
                self._create_tables_if_not_exists(conn)
            finally:
                self.return_connection(conn)
            
        except Exception as e:
            self.connection_pool = None
            raise 

    def get_connection(self):
        if not self.connection_pool:
            raise Exception("O pool de conexões não foi inicializado.")
        return self.connection_pool.getconn()

    def return_connection(self, conn):
        if self.connection_pool and conn:
            self.connection_pool.putconn(conn)
    
    def _create_tables_if_not_exists(self, conn):
        try:
            with conn.cursor() as cur:
                # Tabela de usuários permanece a mesma.
                cur.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    email VARCHAR(120),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
                """)
                
                # ALTERAÇÃO CRÍTICA AQUI:
                # Adicionamos a coluna 'user_id' que faz referência à tabela 'usuarios'.
                # ON DELETE CASCADE significa que se um usuário for deletado,
                # todos os seus contatos também serão.
                cur.execute("""
                CREATE TABLE IF NOT EXISTS contatos (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
                    nome VARCHAR(255) NOT NULL,
                    telefone VARCHAR(50) NOT NULL,
                    email VARCHAR(255),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (user_id, telefone) -- Garante que um usuário não pode ter o mesmo telefone duas vezes.
                );
                """)
                conn.commit()
                print("INFO: Tabelas com estrutura multi-usuário verificadas/criadas.")
        except Exception as e:
            conn.rollback()
            raise
    
    def close_all_connections(self):
        if self.connection_pool:
            self.connection_pool.closeall()

db_manager = DatabaseManager()
