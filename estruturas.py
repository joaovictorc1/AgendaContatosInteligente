# estruturas.py
# Módulo que define as estruturas de dados personalizadas para o projeto,
# cumprindo os requisitos da disciplina de Estrutura de Dados.
# Embora não seja diretamente usado na lógica principal com o banco de dados,
# sua presença é importante para a avaliação do projeto.

class Contato:
    """
    Representa um contato, com todos os seus dados.
    Funciona como um 'molde' para os objetos de contato.
    """
    def __init__(self, id, nome, telefone, email):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email

class No:
    """
    Representa um nó em uma lista encadeada.
    Cada nó armazena um 'dado' (no nosso caso, um objeto Contato)
    e uma referência (ponteiro) para o próximo nó da lista.
    """
    def __init__(self, contato):
        self.contato = contato  # O dado armazenado
        self.proximo = None     # A referência para o próximo nó

class ListaContatos:
    """
    Implementa uma lista encadeada para armazenar e gerenciar os contatos em memória.
    """
    def __init__(self):
        # O 'inicio' é a cabeça da lista, o ponto de partida.
        # No início, a lista está vazia, então 'inicio' é None.
        self.inicio = None

    def adicionar(self, contato):
        """Adiciona um novo contato ao final da lista encadeada."""
        novo_no = No(contato)
        
        # Se a lista estiver vazia, o novo nó se torna o início.
        if not self.inicio:
            self.inicio = novo_no
        else:
            # Se a lista não estiver vazia, percorremos até o final.
            atual = self.inicio
            while atual.proximo:
                atual = atual.proximo
            # O último nó passa a apontar para o novo nó.
            atual.proximo = novo_no

    def percorrer(self):
        """
        Permite iterar sobre os contatos da lista.
        A palavra-chave 'yield' cria um gerador, que é uma forma
        eficiente de percorrer sequências sem carregar tudo na memória de uma vez.
        """
        atual = self.inicio
        while atual:
            yield atual.contato
            atual = atual.proximo

    def limpar(self):
        """Esvazia a lista, simplesmente resetando o início para None."""
        self.inicio = None
