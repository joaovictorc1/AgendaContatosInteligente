# crud_contatos.py
# CORREÇÃO: Todas as funções agora recebem um 'user_id' e o utilizam
# nas queries SQL para garantir que um usuário só acesse seus próprios contatos.

from database import db_manager
from datetime import datetime, timezone

def adicionar_contato(user_id, nome, telefone, email):
    conn = db_manager.get_connection()
    try:
        with conn.cursor() as cur:
            # A query INSERT agora inclui o user_id.
            cur.execute(
                "INSERT INTO contatos (user_id, nome, telefone, email) VALUES (%s, %s, %s, %s)",
                (user_id, nome, telefone, email)
            )
            conn.commit()
            return True, "Contato adicionado com sucesso."
    except Exception as e:
        conn.rollback()
        # O erro de telefone duplicado agora é por usuário.
        if 'contatos_user_id_telefone_key' in str(e):
            return False, "Este telefone já está cadastrado na sua agenda."
        return False, f"Erro ao adicionar contato: {e}"
    finally:
        db_manager.return_connection(conn)

def obter_contatos(user_id):
    conn = db_manager.get_connection()
    try:
        with conn.cursor() as cur:
            # A query SELECT agora filtra pelo user_id.
            cur.execute("SELECT id, nome, telefone, email FROM contatos WHERE user_id = %s ORDER BY nome", (user_id,))
            results = cur.fetchall()
            contatos = [{'id': row[0], 'nome': row[1], 'telefone': row[2], 'email': row[3]} for row in results]
            return contatos
    except Exception as e:
        print(f"Erro ao obter contatos: {e}")
        return []
    finally:
        db_manager.return_connection(conn)

def atualizar_contato(user_id, telefone_antigo, nome, telefone_novo, email):
    conn = db_manager.get_connection()
    try:
        with conn.cursor() as cur:
            # A query UPDATE agora também verifica o user_id, garantindo
            # que um usuário não possa editar o contato de outro.
            cur.execute(
                """
                UPDATE contatos SET nome = %s, telefone = %s, email = %s, updated_at = %s
                WHERE telefone = %s AND user_id = %s
                """,
                (nome, telefone_novo, email, datetime.now(timezone.utc), telefone_antigo, user_id)
            )
            if cur.rowcount == 0:
                return False, "Contato original não encontrado ou você não tem permissão para editá-lo."
            conn.commit()
            return True, "Contato atualizado com sucesso."
    except Exception as e:
        conn.rollback()
        if 'contatos_user_id_telefone_key' in str(e):
            return False, "O novo telefone informado já pertence a outro contato seu."
        return False, f"Erro ao atualizar contato: {e}"
    finally:
        db_manager.return_connection(conn)

def remover_contato_por_telefone(user_id, telefone):
    conn = db_manager.get_connection()
    try:
        with conn.cursor() as cur:
            # A query DELETE agora também verifica o user_id.
            cur.execute("DELETE FROM contatos WHERE telefone = %s AND user_id = %s", (telefone, user_id))
            if cur.rowcount == 0:
                return False, "Contato não encontrado ou você não tem permissão para removê-lo."
            conn.commit()
            return True, "Contato removido com sucesso."
    except Exception as e:
        conn.rollback()
        return False, f"Erro ao remover contato: {e}"
    finally:
        db_manager.return_connection(conn)
