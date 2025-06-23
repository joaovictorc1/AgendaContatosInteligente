# crud_contatos.py
# Módulo com as funções de CRUD para contatos, configurado para PostgreSQL.

from database import db_manager
from datetime import datetime, timezone

def adicionar_contato(nome, telefone, email):
    conn = db_manager.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO contatos (nome, telefone, email) VALUES (%s, %s, %s)",
                (nome, telefone, email)
            )
            conn.commit()
            return True, "Contato adicionado com sucesso."
    except Exception as e:
        conn.rollback()
        if 'contatos_telefone_key' in str(e):
            return False, "Este telefone já está cadastrado."
        return False, f"Erro ao adicionar contato: {e}"
    finally:
        db_manager.return_connection(conn)

def obter_contatos():
    conn = db_manager.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nome, telefone, email FROM contatos ORDER BY nome")
            results = cur.fetchall()
            # Converte os resultados em uma lista de dicionários
            contatos = [{'id': row[0], 'nome': row[1], 'telefone': row[2], 'email': row[3]} for row in results]
            return contatos
    except Exception as e:
        print(f"Erro ao obter contatos: {e}")
        return []
    finally:
        db_manager.return_connection(conn)

def atualizar_contato(telefone_antigo, nome, telefone_novo, email):
    conn = db_manager.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE contatos 
                SET nome = %s, telefone = %s, email = %s, updated_at = %s
                WHERE telefone = %s
                """,
                (nome, telefone_novo, email, datetime.now(timezone.utc), telefone_antigo)
            )
            if cur.rowcount == 0:
                return False, "Contato original não encontrado para atualizar."
            conn.commit()
            return True, "Contato atualizado com sucesso."
    except Exception as e:
        conn.rollback()
        if 'contatos_telefone_key' in str(e):
            return False, "O novo telefone informado já pertence a outro contato."
        return False, f"Erro ao atualizar contato: {e}"
    finally:
        db_manager.return_connection(conn)

def remover_contato_por_telefone(telefone):
    conn = db_manager.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM contatos WHERE telefone = %s", (telefone,))
            if cur.rowcount == 0:
                return False, "Contato não encontrado para remoção."
            conn.commit()
            return True, "Contato removido com sucesso."
    except Exception as e:
        conn.rollback()
        return False, f"Erro ao remover contato: {e}"
    finally:
        db_manager.return_connection(conn)
