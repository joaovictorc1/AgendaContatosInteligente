
import json
import os

ARQUIVO = "contatos.json"
CONTATOS = []

def carregar_contatos():
    global CONTATOS
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            CONTATOS = json.load(f)

def salvar_contatos():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(CONTATOS, f, indent=4, ensure_ascii=False)

def adicionar_contato(nome, telefone, email):
    for c in CONTATOS:
        if c['telefone'] == telefone:
            return False, "Telefone já cadastrado."
    CONTATOS.append({"nome": nome, "telefone": telefone, "email": email})
    return True, "Contato adicionado com sucesso."

def buscar_contatos(chave):
    return [c for c in CONTATOS if chave.lower() in c['nome'].lower() or chave in c['telefone']]

def remover_contato_indice(indice):
    if 0 <= indice < len(CONTATOS):
        del CONTATOS[indice]
        return True, "Contato removido."
    return False, "Índice inválido."

def obter_contatos():
    return CONTATOS[:]
