# auth.py
# Módulo para gerenciar a autenticação de usuários: registro, login,
# hashing de senhas e gerenciamento da sessão do usuário.

import bcrypt
from datetime import datetime, timezone
from database import db_manager

class AuthManager:
    """Gerencia o registro, login e sessão dos usuários."""
    
    def __init__(self):
        self.current_user = None
    
    def _hash_password(self, password: str) -> bytes:
        """Gera um hash seguro para a senha fornecida."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifica se a senha corresponde ao hash armazenado."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def register_user(self, username, password, email=None):
        """Registra um novo usuário no banco de dados."""
        if not username or not password:
            return False, "Usuário e senha são obrigatórios."
        if len(username) < 3:
            return False, "Usuário deve ter pelo menos 3 caracteres."
        if len(password) < 6:
            return False, "Senha deve ter pelo menos 6 caracteres."
        
        password_hash = self._hash_password(password)
        
        conn = db_manager.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO usuarios (username, password_hash, email) VALUES (%s, %s, %s)",
                    (username, password_hash.decode('utf-8'), email)
                )
                conn.commit()
                return True, "Usuário registrado com sucesso!"
        except Exception as e:
            conn.rollback()
            if 'usuarios_username_key' in str(e):
                return False, "Este nome de usuário já está em uso."
            return False, f"Erro ao registrar: {e}"
        finally:
            db_manager.return_connection(conn)

    def login_user(self, username, password):
        """Autentica um usuário e gerencia a sessão."""
        if not username or not password:
            return False, "Usuário e senha são obrigatórios."

        conn = db_manager.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, username, password_hash, email FROM usuarios WHERE username = %s", (username,))
                user_data = cur.fetchone()
                
                if not user_data:
                    return False, "Usuário ou senha inválidos."
                
                user_id, db_username, db_password_hash, db_email = user_data
                
                if not self._verify_password(password, db_password_hash):
                    return False, "Usuário ou senha inválidos."
                
                # Atualiza o timestamp do último login
                cur.execute(
                    "UPDATE usuarios SET last_login = %s WHERE id = %s",
                    (datetime.now(timezone.utc), user_id)
                )
                conn.commit()
                
                self.current_user = {'id': user_id, 'username': db_username, 'email': db_email}
                return True, f"Login bem-sucedido! Bem-vindo, {db_username}!"
        except Exception as e:
            conn.rollback()
            return False, f"Erro no servidor: {e}"
        finally:
            db_manager.return_connection(conn)
            
    def logout_user(self):
        """Faz o logout do usuário atual."""
        self.current_user = None
    
    def is_logged_in(self):
        """Verifica se há um usuário logado."""
        return self.current_user is not None
    
    def get_current_user(self):
        """Retorna os dados do usuário logado."""
        return self.current_user
    
    def change_password(self, old_password, new_password):
        """Altera a senha do usuário logado."""
        if not self.is_logged_in():
            return False, "Nenhum usuário logado."
        if len(new_password) < 6:
            return False, "A nova senha deve ter pelo menos 6 caracteres."

        conn = db_manager.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT password_hash FROM usuarios WHERE id = %s", (self.current_user['id'],))
                current_hash = cur.fetchone()[0]
                
                if not self._verify_password(old_password, current_hash):
                    return False, "Senha atual incorreta."
                
                new_hash = self._hash_password(new_password)
                cur.execute(
                    "UPDATE usuarios SET password_hash = %s WHERE id = %s",
                    (new_hash.decode('utf-8'), self.current_user['id'])
                )
                conn.commit()
                return True, "Senha alterada com sucesso!"
        except Exception as e:
            conn.rollback()
            return False, f"Erro ao alterar senha: {e}"
        finally:
            db_manager.return_connection(conn)

# Instância global
auth_manager = AuthManager()
