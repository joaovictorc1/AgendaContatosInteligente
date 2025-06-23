# app.py
# CORREÇÃO: As rotas da API agora pegam o ID do usuário da sessão
# e o passam para as funções do backend.

from flask import Flask, render_template, request, jsonify, session
from datetime import timedelta

from database import db_manager
import crud_contatos 
import auth

app = Flask(__name__)
app.secret_key = 'chave-secreta-para-o-projeto-integrador' 
app.permanent_session_lifetime = timedelta(days=1)

# --- Rotas de Autenticação (sem alterações) ---
@app.route('/')
def index(): return render_template('index.html')

@app.route('/check_status')
def check_status():
    if 'user' in session:
        return jsonify({'logged_in': True, 'user': session['user']})
    return jsonify({'logged_in': False})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    success, message = auth.auth_manager.register_user(data.get('username'), data.get('password'), data.get('email'))
    return jsonify({'success': success, 'message': message})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    success, message = auth.auth_manager.login_user(data.get('username'), data.get('password'))
    if success:
        session.permanent = True
        session['user'] = auth.auth_manager.get_current_user()
        return jsonify({'success': True, 'user': session['user']})
    return jsonify({'success': False, 'message': message})

@app.route('/logout')
def logout():
    session.pop('user', None)
    return jsonify({'success': True})

# --- API para os Contatos (com alterações) ---

def get_current_user_id():
    """Função auxiliar para pegar o user_id da sessão."""
    return session.get('user', {}).get('id')

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    user_id = get_current_user_id()
    if not user_id: return jsonify({'success': False, 'message': 'Não autorizado'}), 401
    
    # Passa o user_id para a função do backend.
    contacts = crud_contatos.obter_contatos(user_id)
    return jsonify({'success': True, 'contacts': contacts})

@app.route('/api/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    user_id = get_current_user_id()
    if not user_id: return jsonify({'success': False, 'message': 'Não autorizado'}), 401
    
    # Para buscar um contato, primeiro pegamos todos os contatos do usuário
    # e depois filtramos pelo ID.
    contacts = crud_contatos.obter_contatos(user_id)
    contact = next((c for c in contacts if c['id'] == contact_id), None)
    
    if contact:
        return jsonify({'success': True, 'contact': contact})
    return jsonify({'success': False, 'message': 'Contato não encontrado'}), 404

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    user_id = get_current_user_id()
    if not user_id: return jsonify({'success': False, 'message': 'Não autorizado'}), 401
        
    data = request.get_json()
    # Passa o user_id para a função do backend.
    success, message = crud_contatos.adicionar_contato(user_id, data['nome'], data['telefone'], data.get('email'))
    return jsonify({'success': success, 'message': message})

@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    user_id = get_current_user_id()
    if not user_id: return jsonify({'success': False, 'message': 'Não autorizado'}), 401
    
    data = request.get_json()
    contacts = crud_contatos.obter_contatos(user_id)
    contact_original = next((c for c in contacts if c['id'] == contact_id), None)
    if not contact_original:
         return jsonify({'success': False, 'message': 'Contato original não encontrado'}), 404
    
    # Passa o user_id para a função do backend.
    success, message = crud_contatos.atualizar_contato(
        user_id, contact_original['telefone'], data['nome'], data['telefone'], data.get('email')
    )
    return jsonify({'success': success, 'message': message})

@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    user_id = get_current_user_id()
    if not user_id: return jsonify({'success': False, 'message': 'Não autorizado'}), 401
        
    contacts = crud_contatos.obter_contatos(user_id)
    contact_to_delete = next((c for c in contacts if c['id'] == contact_id), None)
    if not contact_to_delete:
         return jsonify({'success': False, 'message': 'Contato não encontrado'}), 404
    
    # Passa o user_id para a função do backend.
    success, message = crud_contatos.remover_contato_por_telefone(user_id, contact_to_delete['telefone'])
    return jsonify({'success': success, 'message': message})

# --- Ponto de Entrada da Aplicação ---
if __name__ == '__main__':
    try:
        db_manager.init_connection_pool()
    except Exception as e:
        print(f"ERRO CRÍTICO AO INICIALIZAR BANCO DE DADOS: {e}")
        exit()

    app.run(debug=True, port=5000)
