
import tkinter as tk
from tkinter import messagebox, simpledialog
import contatos

contatos.carregar_contatos()

def atualizar_lista():
    lista_contatos.delete(0, tk.END)
    for c in contatos.obter_contatos():
        lista_contatos.insert(tk.END, f"{c['nome']} | {c['telefone']} | {c['email']}")

def adicionar():
    nome = entrada_nome.get().strip()
    telefone = entrada_telefone.get().strip()
    email = entrada_email.get().strip()
    if not nome or not telefone:
        messagebox.showwarning("Erro", "Nome e telefone são obrigatórios!")
        return
    sucesso, msg = contatos.adicionar_contato(nome, telefone, email)
    if sucesso:
        contatos.salvar_contatos()
        atualizar_lista()
        entrada_nome.delete(0, tk.END)
        entrada_telefone.delete(0, tk.END)
        entrada_email.delete(0, tk.END)
    messagebox.showinfo("Info", msg)

def buscar():
    chave = simpledialog.askstring("Buscar", "Digite nome ou telefone:")
    if chave:
        resultados = contatos.buscar_contatos(chave)
        if resultados:
            resultado = "\n".join([f"{c['nome']} | {c['telefone']} | {c['email']}" for c in resultados])
            messagebox.showinfo("Resultados", resultado)
        else:
            messagebox.showinfo("Busca", "Nenhum contato encontrado.")

def remover():
    sel = lista_contatos.curselection()
    if sel:
        idx = sel[0]
        contato = contatos.obter_contatos()[idx]
        confirmar = messagebox.askyesno("Remover", f"Remover {contato['nome']}?")
        if confirmar:
            sucesso, msg = contatos.remover_contato_indice(idx)
            if sucesso:
                contatos.salvar_contatos()
                atualizar_lista()
            messagebox.showinfo("Info", msg)

janela = tk.Tk()
janela.title("Gerenciador de Contatos")

frame_entrada = tk.Frame(janela)
frame_entrada.pack(padx=10, pady=5)

entrada_nome = tk.Entry(frame_entrada, width=30)
entrada_telefone = tk.Entry(frame_entrada, width=30)
entrada_email = tk.Entry(frame_entrada, width=30)

entrada_nome.grid(row=0, column=1, padx=5, pady=2)
entrada_telefone.grid(row=1, column=1, padx=5, pady=2)
entrada_email.grid(row=2, column=1, padx=5, pady=2)

tk.Label(frame_entrada, text="Nome:").grid(row=0, column=0, sticky=tk.W)
tk.Label(frame_entrada, text="Telefone:").grid(row=1, column=0, sticky=tk.W)
tk.Label(frame_entrada, text="Email:").grid(row=2, column=0, sticky=tk.W)

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=5)

tk.Button(frame_botoes, text="Adicionar", command=adicionar).grid(row=0, column=0, padx=5)
tk.Button(frame_botoes, text="Buscar", command=buscar).grid(row=0, column=1, padx=5)
tk.Button(frame_botoes, text="Remover", command=remover).grid(row=0, column=2, padx=5)
tk.Button(frame_botoes, text="Sair", command=janela.quit).grid(row=0, column=3, padx=5)

lista_contatos = tk.Listbox(janela, width=60)
lista_contatos.pack(padx=10, pady=10)

atualizar_lista()
janela.mainloop()
