# app.py
# Servidor web com Flask. Este é o único arquivo que você precisa executar.
# Versão corrigida para conectar ao Neon/PostgreSQL.

import sqlite3
from flask import Flask, render_template, request, jsonify, session
from datetime import timedelta

# Importa os módulos de backend que já estavam prontos
from database import db_manager
import crud_contatos 
import auth

# --- Configuração da Aplicação Flask ---
app = Flask(__name__)
# Chave secreta necessária para gerenciar sessões (login)
app.secret_key = 'chave-secreta-para-o-projeto-integrador' 
# Define que a sessão (login) dura 1 dia.
app.permanent_session_lifetime = timedelta(days=1)

# --- Rotas da Interface e Autenticação ---

@app.route('/')
def index():
    """Renderiza a página HTML principal."""
    return render_template('index.html')

@app.route('/check_status')
def check_status():
    """Verifica se o usuário está logado na sessão."""
    if 'user' in session:
        return jsonify({'logged_in': True, 'user': session['user']})
    return jsonify({'logged_in': False})

@app.route('/register', methods=['POST'])
def register():
    """Endpoint para registrar um novo usuário."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    success, message = auth.auth_manager.register_user(username, password, email)
    
    return jsonify({'success': success, 'message': message})

@app.route('/login', methods=['POST'])
def login():
    """Endpoint para autenticar um usuário."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    success, message = auth.auth_manager.login_user(username, password)
    
    if success:
        session.permanent = True
        session['user'] = auth.auth_manager.get_current_user()
        return jsonify({'success': True, 'user': session['user']})
        
    return jsonify({'success': False, 'message': message})

@app.route('/logout')
def logout():
    """Endpoint para fazer logout."""
    # A classe AuthManager não tem mais o método logout_user, a lógica agora é só limpar a sessão.
    session.pop('user', None)
    return jsonify({'success': True})

# --- API para os Contatos (CRUD) ---

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    """Retorna a lista de todos os contatos em formato JSON."""
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Não autorizado'}), 401
        
    contacts = crud_contatos.obter_contatos()
    return jsonify({'success': True, 'contacts': contacts})

@app.route('/api/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    """Retorna os dados de um contato específico."""
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Não autorizado'}), 401
    
    contacts = crud_contatos.obter_contatos()
    contact = next((c for c in contacts if c['id'] == contact_id), None)
    
    if contact:
        return jsonify({'success': True, 'contact': contact})
    return jsonify({'success': False, 'message': 'Contato não encontrado'}), 404

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    """Adiciona um novo contato."""
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Não autorizado'}), 401
        
    data = request.get_json()
    success, message = crud_contatos.adicionar_contato(data['nome'], data['telefone'], data.get('email'))
    return jsonify({'success': success, 'message': message})

@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    """Atualiza um contato existente."""
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Não autorizado'}), 401
    
    data = request.get_json()
    contacts = crud_contatos.obter_contatos()
    contact_original = next((c for c in contacts if c['id'] == contact_id), None)
    if not contact_original:
         return jsonify({'success': False, 'message': 'Contato original não encontrado'}), 404
    
    success, message = crud_contatos.atualizar_contato(
        contact_original['telefone'], 
        data['nome'], 
        data['telefone'], 
        data.get('email')
    )
    return jsonify({'success': success, 'message': message})

@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """Exclui um contato."""
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Não autorizado'}), 401
        
    contacts = crud_contatos.obter_contatos()
    contact_to_delete = next((c for c in contacts if c['id'] == contact_id), None)
    if not contact_to_delete:
         return jsonify({'success': False, 'message': 'Contato não encontrado'}), 404
         
    success, message = crud_contatos.remover_contato_por_telefone(contact_to_delete['telefone'])
    return jsonify({'success': success, 'message': message})


# --- Ponto de Entrada da Aplicação ---
if __name__ == '__main__':
    # CORREÇÃO APLICADA AQUI:
    # Em vez de importar 'init_database', importamos o objeto 'db_manager'
    # e chamamos seu método de inicialização.
    try:
        db_manager.init_connection_pool()
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"ERRO CRÍTICO AO INICIALIZAR BANCO DE DADOS: {e}")
        print("Verifique sua internet e a configuração do arquivo .env")
        print("Se o erro for 'permission denied', execute o comando GRANT no SQL Editor do Neon.")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        exit()

    # Inicia o servidor web
    app.run(debug=True, port=5000)

