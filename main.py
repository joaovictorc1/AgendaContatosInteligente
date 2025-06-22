# main.py
# Ponto de entrada da aplicação. Gerencia a interface gráfica e o fluxo
# entre a tela de login e a agenda principal.

import tkinter as tk
from tkinter import messagebox, simpledialog
from auth import auth_manager
import crud_contatos

class LoginWindow:
    """Janela de login e registro de usuários."""
    
    def __init__(self, root, on_success_callback):
        self.on_success = on_success_callback
        self.window = tk.Toplevel(root)
        self.window.title("Login - Agenda de Contatos")
        self.window.geometry("400x350")
        self.window.resizable(False, False)
        
        # Garante que esta janela fique em foco
        self.window.transient(root)
        self.window.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura os widgets da interface de login."""
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        tk.Label(main_frame, text="Agenda de Contatos", font=("Arial", 18, "bold")).pack(pady=(0, 20))
        
        tk.Label(main_frame, text="Usuário:", font=("Arial", 10)).pack(anchor="w")
        self.username_entry = tk.Entry(main_frame, width=30, font=("Arial", 12))
        self.username_entry.pack(pady=(0, 10), fill="x")
        
        tk.Label(main_frame, text="Senha:", font=("Arial", 10)).pack(anchor="w")
        self.password_entry = tk.Entry(main_frame, width=30, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=(0, 20), fill="x")

        # Bind da tecla Enter para o login
        self.password_entry.bind('<Return>', lambda event: self.attempt_login())
        
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)
        
        login_btn = tk.Button(button_frame, text="Login", command=self.attempt_login, font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", relief="flat")
        login_btn.pack(side="left", fill="x", expand=True, ipady=5, padx=(0, 5))
        
        register_btn = tk.Button(button_frame, text="Registrar", command=self.open_register_window, font=("Arial", 10, "bold"), bg="#2196F3", fg="white", relief="flat")
        register_btn.pack(side="right", fill="x", expand=True, ipady=5, padx=(5, 0))
        
        self.username_entry.focus()
    
    def attempt_login(self):
        """Tenta autenticar o usuário com os dados inseridos."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Campos Vazios", "Usuário e senha são obrigatórios.", parent=self.window)
            return
        
        success, message = auth_manager.login_user(username, password)
        
        if success:
            messagebox.showinfo("Sucesso", message, parent=self.window)
            self.window.destroy()
            self.on_success()
        else:
            messagebox.showerror("Falha no Login", message, parent=self.window)
            self.password_entry.delete(0, tk.END)

    def open_register_window(self):
        RegisterWindow(self.window)


class RegisterWindow:
    """Janela de registro de um novo usuário."""
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Registrar Novo Usuário")
        self.window.geometry("400x350")
        self.window.resizable(False, False)
        
        self.window.transient(parent)
        self.window.grab_set()

        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        tk.Label(main_frame, text="Criar Nova Conta", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        tk.Label(main_frame, text="Usuário (mín. 3 caracteres):").pack(anchor="w")
        self.username_entry = tk.Entry(main_frame, font=("Arial", 12))
        self.username_entry.pack(fill="x", pady=(0, 10))

        tk.Label(main_frame, text="Senha (mín. 6 caracteres):").pack(anchor="w")
        self.password_entry = tk.Entry(main_frame, show="*", font=("Arial", 12))
        self.password_entry.pack(fill="x", pady=(0, 10))

        tk.Label(main_frame, text="Email (opcional):").pack(anchor="w")
        self.email_entry = tk.Entry(main_frame, font=("Arial", 12))
        self.email_entry.pack(fill="x", pady=(0, 20))

        register_btn = tk.Button(main_frame, text="Registrar", command=self.attempt_register, font=("Arial", 10, "bold"), bg="#2196F3", fg="white", relief="flat")
        register_btn.pack(fill="x", ipady=5)

        self.username_entry.focus()

    def attempt_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        email = self.email_entry.get().strip() or None

        success, message = auth_manager.register_user(username, password, email)
        
        if success:
            messagebox.showinfo("Sucesso", message + "\n\nAgora você pode fazer o login.", parent=self.window)
            self.window.destroy()
        else:
            messagebox.showerror("Erro no Registro", message, parent=self.window)


class MainApplication:
    """Aplicação principal da agenda, exibida após o login."""
    
    def __init__(self, root):
        self.root = root
        self.setup_main_ui()
    
    def setup_main_ui(self):
        self.root.deiconify()
        user_info = auth_manager.get_current_user()
        self.root.title(f"Agenda de Contatos - Usuário: {user_info['username']}")
        self.root.geometry("800x600")

        # Limpa widgets antigos, se houver
        for widget in self.root.winfo_children():
            widget.destroy()

        # Barra de Status/Menu Superior
        status_frame = tk.Frame(self.root, bg="#f0f0f0", relief="solid", borderwidth=1)
        status_frame.pack(fill="x", side="top", ipady=5)
        
        tk.Label(status_frame, text=f"Logado como: {user_info['username']}", bg="#f0f0f0", font=("Arial", 9)).pack(side="left", padx=10)
        
        tk.Button(status_frame, text="Logout", command=self.logout, font=("Arial", 8, "bold"), bg="#f44336", fg="white", relief="flat").pack(side="right", padx=10)
        tk.Button(status_frame, text="Alterar Senha", command=self.open_change_password_window, font=("Arial", 8, "bold"), bg="#FF9800", fg="white", relief="flat").pack(side="right")

        # Frame de Entrada de Dados
        entry_frame = tk.Frame(self.root, pady=10, padx=10)
        entry_frame.pack(fill="x")
        
        tk.Label(entry_frame, text="Nome:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.entry_nome = tk.Entry(entry_frame, width=40)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(entry_frame, text="Telefone:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.entry_telefone = tk.Entry(entry_frame, width=40)
        self.entry_telefone.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(entry_frame, text="Email:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.entry_email = tk.Entry(entry_frame, width=40)
        self.entry_email.grid(row=2, column=1, padx=5, pady=2)

        # Frame de Botões de Ação
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Adicionar", command=self.add_contact, width=12).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Buscar", command=self.search_contact, width=12).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Editar", command=self.edit_contact, width=12).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Remover", command=self.remove_contact, width=12).grid(row=0, column=3, padx=5)
        
        # Listbox para exibir contatos
        list_frame = tk.Frame(self.root, padx=10, pady=10)
        list_frame.pack(fill="both", expand=True)
        self.contact_listbox = tk.Listbox(list_frame, height=15, font=("Courier", 10))
        self.contact_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.contact_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.contact_listbox.config(yscrollcommand=scrollbar.set)
        
        self.update_contact_list()
    
    def update_contact_list(self):
        """Atualiza a lista de contatos na tela."""
        self.contact_listbox.delete(0, tk.END)
        self.all_contacts = crud_contatos.obter_contatos()
        for c in self.all_contacts:
            self.contact_listbox.insert(tk.END, f"{c['nome']:<30} | {c['telefone']:<15} | {c['email']}")
    
    def add_contact(self):
        nome = self.entry_nome.get().strip()
        telefone = self.entry_telefone.get().strip()
        email = self.entry_email.get().strip()
        
        if not nome or not telefone:
            messagebox.showwarning("Erro", "Nome e telefone são obrigatórios!", parent=self.root)
            return
        
        success, msg = crud_contatos.adicionar_contato(nome, telefone, email)
        if success:
            self.update_contact_list()
            self.entry_nome.delete(0, tk.END)
            self.entry_telefone.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
        messagebox.showinfo("Info", msg, parent=self.root)
    
    def search_contact(self):
        key = simpledialog.askstring("Buscar", "Digite nome ou telefone:", parent=self.root)
        if key:
            results = crud_contatos.buscar_contatos(key)
            if results:
                info = "\n".join([f"{c['nome']} | {c['telefone']} | {c['email']}" for c in results])
                messagebox.showinfo("Resultados", info, parent=self.root)
            else:
                messagebox.showinfo("Busca", "Nenhum contato encontrado.", parent=self.root)
    
    def edit_contact(self):
        selected_indices = self.contact_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Atenção", "Selecione um contato para editar.", parent=self.root)
            return
        
        selected_contact = self.all_contacts[selected_indices[0]]
        EditContactWindow(self.root, selected_contact, self.update_contact_list)

    def remove_contact(self):
        selected_indices = self.contact_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Atenção", "Selecione um contato para remover.", parent=self.root)
            return
        
        contact_to_remove = self.all_contacts[selected_indices[0]]
        
        confirm = messagebox.askyesno("Confirmar Remoção", f"Remover {contact_to_remove['nome']}?", parent=self.root)
        if confirm:
            success, msg = crud_contatos.remover_contato_por_telefone(contact_to_remove['telefone'])
            if success:
                self.update_contact_list()
            messagebox.showinfo("Info", msg, parent=self.root)
    
    def open_change_password_window(self):
        ChangePasswordWindow(self.root)

    def logout(self):
        if messagebox.askyesno("Logout", "Deseja realmente sair?", parent=self.root):
            auth_manager.logout_user()
            # Esconde a janela principal e reinicia o fluxo
            self.root.withdraw()
            start_app()

class EditContactWindow:
    def __init__(self, parent, contact_data, on_success_callback):
        self.contact = contact_data
        self.on_success = on_success_callback
        self.window = tk.Toplevel(parent)
        self.window.title("Editar Contato")
        self.window.geometry("400x250")
        self.window.resizable(False, False)
        
        self.window.transient(parent)
        self.window.grab_set()

        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        tk.Label(main_frame, text="Editar Contato", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        tk.Label(main_frame, text="Nome:").pack(anchor="w")
        self.nome_entry = tk.Entry(main_frame, font=("Arial", 12))
        self.nome_entry.insert(0, self.contact['nome'])
        self.nome_entry.pack(fill="x", pady=(0, 10))

        tk.Label(main_frame, text="Telefone:").pack(anchor="w")
        self.telefone_entry = tk.Entry(main_frame, font=("Arial", 12))
        self.telefone_entry.insert(0, self.contact['telefone'])
        self.telefone_entry.pack(fill="x", pady=(0, 10))

        tk.Label(main_frame, text="Email:").pack(anchor="w")
        self.email_entry = tk.Entry(main_frame, font=("Arial", 12))
        self.email_entry.insert(0, self.contact.get('email', ''))
        self.email_entry.pack(fill="x", pady=(0, 20))

        save_btn = tk.Button(main_frame, text="Salvar Alterações", command=self.save_changes, font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", relief="flat")
        save_btn.pack(fill="x", ipady=5)

    def save_changes(self):
        new_name = self.nome_entry.get().strip()
        new_phone = self.telefone_entry.get().strip()
        new_email = self.email_entry.get().strip()

        if not new_name or not new_phone:
            messagebox.showerror("Erro", "Nome e telefone são obrigatórios.", parent=self.window)
            return

        success, msg = crud_contatos.atualizar_contato(
            self.contact['telefone'],
            nome=new_name,
            telefone_novo=new_phone,
            email=new_email
        )
        messagebox.showinfo("Info", msg, parent=self.window)
        if success:
            self.on_success()
            self.window.destroy()

class ChangePasswordWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Alterar Senha")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")
        
        tk.Label(main_frame, text="Alterar Senha", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        tk.Label(main_frame, text="Senha Atual:").pack(anchor="w")
        self.old_pass_entry = tk.Entry(main_frame, show="*", font=("Arial", 12))
        self.old_pass_entry.pack(fill="x", pady=(0, 10))
        
        tk.Label(main_frame, text="Nova Senha:").pack(anchor="w")
        self.new_pass_entry = tk.Entry(main_frame, show="*", font=("Arial", 12))
        self.new_pass_entry.pack(fill="x", pady=(0, 10))

        tk.Label(main_frame, text="Confirmar Nova Senha:").pack(anchor="w")
        self.confirm_pass_entry = tk.Entry(main_frame, show="*", font=("Arial", 12))
        self.confirm_pass_entry.pack(fill="x", pady=(0, 20))
        
        change_btn = tk.Button(main_frame, text="Alterar Senha", command=self.attempt_change, font=("Arial", 10, "bold"), bg="#FF9800", fg="white", relief="flat")
        change_btn.pack(fill="x", ipady=5)
        
        self.old_pass_entry.focus()

    def attempt_change(self):
        old_pass = self.old_pass_entry.get()
        new_pass = self.new_pass_entry.get()
        confirm_pass = self.confirm_pass_entry.get()

        if not all([old_pass, new_pass, confirm_pass]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.", parent=self.window)
            return
        
        if new_pass != confirm_pass:
            messagebox.showerror("Erro", "A nova senha e a confirmação não coincidem.", parent=self.window)
            return

        success, msg = auth_manager.change_password(old_pass, new_pass)
        messagebox.showinfo("Info", msg, parent=self.window)
        if success:
            self.window.destroy()

def start_app():
    """Inicializa a aplicação, mostrando a janela de login."""
    try:
        from database import db_manager
        # Apenas para forçar a inicialização e verificar a conexão
        conn = db_manager.get_connection()
        db_manager.return_connection(conn)
        print("Conexão com o banco de dados verificada com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro Crítico de Conexão", 
                           f"Não foi possível conectar ao banco de dados:\n{e}\n\n"
                           "Verifique sua conexão com a internet e a configuração do arquivo .env.")
        root.quit()
        return

    LoginWindow(root, lambda: MainApplication(root))

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() # Oculta a janela principal inicialmente
    
    start_app()
    
    root.mainloop()

