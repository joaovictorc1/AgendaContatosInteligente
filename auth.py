# auth.py
# Módulo de autenticação configurado para PostgreSQL.

import bcrypt
from datetime import datetime, timezone
from database import db_manager

class AuthManager:
    def __init__(self):
        self.current_user = None
    
    def _hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
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
                
                self.current_user = {'id': user_id, 'username': db_username, 'email': db_email}
                return True, f"Login bem-sucedido! Bem-vindo, {db_username}!"
        except Exception as e:
            return False, f"Erro no servidor durante o login: {e}"
        finally:
            db_manager.return_connection(conn)
            
    def get_current_user(self):
        return self.current_user

# Instância global
auth_manager = AuthManager()
