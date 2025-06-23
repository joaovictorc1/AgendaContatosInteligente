# crud_contatos.py
# Adaptado para usar SQLite. A principal mudança é o placeholder '?' no lugar de '%s'.

from database import get_db_connection
from datetime import datetime

def adicionar_contato(nome, telefone, email):
    """Adiciona um novo contato ao banco de dados."""
    conn = get_db_connection()
    try:
        with conn:
            conn.execute(
                "INSERT INTO contatos (nome, telefone, email) VALUES (?, ?, ?)",
                (nome, telefone, email)
            )
        return True, "Contato adicionado com sucesso."
    except sqlite3.IntegrityError:
        return False, "Erro: Este telefone já está cadastrado."
    except Exception as e:
        return False, f"Erro ao adicionar contato: {e}"
    finally:
        conn.close()

def obter_contatos():
    """Busca e retorna todos os contatos em ordem alfabética."""
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT id, nome, telefone, email FROM contatos ORDER BY nome")
        # Converte os resultados em uma lista de dicionários
        contatos = [dict(row) for row in cursor.fetchall()]
        return contatos
    except Exception as e:
        print(f"Erro ao obter contatos: {e}")
        return []
    finally:
        conn.close()

def buscar_contatos(chave):
    """Busca contatos por nome ou telefone."""
    conn = get_db_connection()
    termo_busca = f"%{chave}%"
    try:
        cursor = conn.execute(
            "SELECT id, nome, telefone, email FROM contatos WHERE nome LIKE ? OR telefone LIKE ? ORDER BY nome",
            (termo_busca, termo_busca)
        )
        contatos = [dict(row) for row in cursor.fetchall()]
        return contatos
    except Exception as e:
        print(f"Erro ao buscar contatos: {e}")
        return []
    finally:
        conn.close()

def remover_contato_por_telefone(telefone):
    """Remove um contato do banco usando o telefone."""
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.execute("DELETE FROM contatos WHERE telefone = ?", (telefone,))
            if cursor.rowcount == 0:
                return False, "Contato não encontrado para remoção."
        return True, "Contato removido com sucesso."
    except Exception as e:
        return False, f"Erro ao remover contato: {e}"
    finally:
        conn.close()

def atualizar_contato(telefone_antigo, nome, telefone_novo, email):
    """Atualiza os dados de um contato existente."""
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.execute(
                """
                UPDATE contatos SET nome = ?, telefone = ?, email = ?, updated_at = ?
                WHERE telefone = ?
                """,
                (nome, telefone_novo, email, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), telefone_antigo)
            )
            if cursor.rowcount == 0:
                return False, "Contato original não encontrado para atualizar."
        return True, "Contato atualizado com sucesso."
    except sqlite3.IntegrityError:
        return False, "O novo telefone informado já pertence a outro contato."
    except Exception as e:
        return False, f"Erro ao atualizar contato: {e}"
    finally:
        conn.close()
