# auth.py
# Adaptado para usar SQLite. A principal mudança é o placeholder '?' no lugar de '%s'.

import bcrypt
from datetime import datetime
from database import get_db_connection

class AuthManager:
    """Gerencia o registro, login e sessão dos usuários com SQLite."""
    
    def __init__(self):
        self.current_user = None
    
    def _hash_password(self, password: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def register_user(self, username, password, email=None):
        if not username or not password:
            return False, "Usuário e senha são obrigatórios."
        if len(username) < 3:
            return False, "Usuário deve ter pelo menos 3 caracteres."
        if len(password) < 6:
            return False, "Senha deve ter pelo menos 6 caracteres."
        
        password_hash = self._hash_password(password)
        conn = get_db_connection()
        try:
            with conn:
                conn.execute(
                    "INSERT INTO usuarios (username, password_hash, email) VALUES (?, ?, ?)",
                    (username, password_hash.decode('utf-8'), email)
                )
            return True, "Usuário registrado com sucesso!"
        except sqlite3.IntegrityError:
            return False, "Este nome de usuário já está em uso."
        except Exception as e:
            return False, f"Erro ao registrar: {e}"
        finally:
            conn.close()

    def login_user(self, username, password):
        if not username or not password:
            return False, "Usuário e senha são obrigatórios."

        conn = get_db_connection()
        try:
            cursor = conn.execute("SELECT id, username, password_hash, email FROM usuarios WHERE username = ?", (username,))
            user_data = cursor.fetchone()
            
            if not user_data:
                return False, "Usuário ou senha inválidos."
            
            user_dict = dict(user_data)
            
            if not self._verify_password(password, user_dict['password_hash']):
                return False, "Usuário ou senha inválidos."
            
            self.current_user = {'id': user_dict['id'], 'username': user_dict['username'], 'email': user_dict['email']}
            return True, f"Login bem-sucedido! Bem-vindo, {user_dict['username']}!"
        except Exception as e:
            return False, f"Erro no servidor: {e}"
        finally:
            conn.close()
            
    def logout_user(self):
        self.current_user = None
    
    def is_logged_in(self):
        return self.current_user is not None
    
    def get_current_user(self):
        return self.current_user
    
    def change_password(self, old_password, new_password):
        if not self.is_logged_in():
            return False, "Nenhum usuário logado."
        if len(new_password) < 6:
            return False, "A nova senha deve ter pelo menos 6 caracteres."

        conn = get_db_connection()
        try:
            cursor = conn.execute("SELECT password_hash FROM usuarios WHERE id = ?", (self.current_user['id'],))
            current_hash = cursor.fetchone()[0]
            
            if not self._verify_password(old_password, current_hash):
                return False, "Senha atual incorreta."
            
            new_hash = self._hash_password(new_password)
            with conn:
                conn.execute(
                    "UPDATE usuarios SET password_hash = ? WHERE id = ?",
                    (new_hash.decode('utf-8'), self.current_user['id'])
                )
            return True, "Senha alterada com sucesso!"
        except Exception as e:
            return False, f"Erro ao alterar senha: {e}"
        finally:
            conn.close()

# Instância global
auth_manager = AuthManager()
