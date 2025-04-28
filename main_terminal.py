import contatos

def menu():
    print("\n==== Agenda de Contatos ====")
    print("1. Adicionar contato")
    print("2. Buscar contato")
    print("3. Remover contato")
    print("4. Listar contatos")
    print("5. Sair")
    print("============================")

def main():
    contatos.carregar_contatos()

    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ").strip()
            telefone = input("Telefone: ").strip()
            email = input("Email: ").strip()
            sucesso, mensagem = contatos.adicionar_contato(nome, telefone, email)
            print(mensagem)
            contatos.salvar_contatos()

        elif opcao == "2":
            chave = input("Digite o nome ou telefone para buscar: ").strip()
            resultados = contatos.buscar_contatos(chave)
            if resultados:
                print("\nResultados encontrados:")
                for c in resultados:
                    print(f"{c['nome']} | {c['telefone']} | {c['email']}")
            else:
                print("Nenhum contato encontrado.")

        elif opcao == "3":
            contatos_lista = contatos.obter_contatos()
            for idx, c in enumerate(contatos_lista):
                print(f"{idx} - {c['nome']} | {c['telefone']} | {c['email']}")
            try:
                indice = int(input("Digite o número do contato a remover: "))
                sucesso, mensagem = contatos.remover_contato_indice(indice)
                print(mensagem)
                contatos.salvar_contatos()
            except ValueError:
                print("Índice inválido.")

        elif opcao == "4":
            contatos_lista = contatos.obter_contatos()
            if not contatos_lista:
                print("Nenhum contato cadastrado.")
            else:
                print("\nLista de contatos:")
                for c in contatos_lista:
                    print(f"{c['nome']} | {c['telefone']} | {c['email']}")

        elif opcao == "5":
            print("Saindo da agenda. Até mais!")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
