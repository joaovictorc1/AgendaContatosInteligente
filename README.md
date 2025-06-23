# Agenda de Contatos Inteligente (Aplicação Web)
## Sobre o Projeto

Este projeto consiste em uma agenda de contatos completa, desenvolvida como uma aplicação web moderna para o Projeto Integrador do curso. A aplicação utiliza Python com o framework Flask para o backend e é conectada a um banco de dados PostgreSQL hospedado na nuvem (Neon), garantindo que os dados sejam persistentes e acessíveis de qualquer lugar.

A interface do usuário foi construída com HTML e Tailwind CSS, resultando em um design limpo, responsivo e com um elegante tema escuro padrão.


## Funcionalidades Principais

    Autenticação de Usuários: Sistema de login completo com registro de novas contas e criptografia de senhas (bcrypt) para garantir a segurança.

    Arquitetura Multi-usuário: Cada usuário tem acesso apenas aos seus próprios contatos, garantindo a privacidade e a separação dos dados.

    Gerenciamento de Contatos (CRUD): Funcionalidades completas para Adicionar, Ler, Atualizar e Deletar contatos.

    Busca Dinâmica: Um campo de busca que filtra a lista de contatos em tempo real, conforme o usuário digita.

    Design Responsivo com Modo Escuro: A interface se adapta a diferentes tamanhos de tela e já vem com um tema escuro padrão para maior conforto visual.

    Persistência de Dados na Nuvem: Utiliza um banco de dados PostgreSQL (Neon) para armazenar todas as informações de forma segura e online.

## Estrutura do Projeto

O código é modularizado para facilitar a manutenção e o entendimento:

    app.py: O coração da aplicação. Contém o servidor web Flask e todas as rotas da API. É este o arquivo que deve ser executado.

    database.py: Gerencia a conexão com o banco de dados PostgreSQL e a criação das tabelas.

    auth.py: Contém toda a lógica de autenticação (registro, login, segurança de senha).

    crud_contatos.py: Possui as funções para manipular os dados dos contatos no banco.

    templates/index.html: Arquivo único que contém toda a estrutura visual e o JavaScript da interface.

    estruturas.py: Implementa uma Lista Encadeada, cumprindo um dos requisitos acadêmicos da disciplina de Estrutura de Dados.

## Tecnologias Utilizadas

    Backend: Python 3, Flask

    Frontend: HTML5, Tailwind CSS, JavaScript

    Banco de Dados: PostgreSQL (hospedado no Neon)

    Bibliotecas Python: psycopg2-binary, bcrypt, python-dotenv

## Como Executar

Siga os passos abaixo para rodar o projeto em um ambiente local.

    1. Pré-requisitos:
    
        Python 3.8+
    
        Git
    
    2. Configuração do Ambiente:
    
    # Clone o repositório para a sua máquina
    git clone 
    
    # Navegue até a pasta do projeto
    cd 
    
    # Crie e ative um ambiente virtual (altamente recomendado)
    python -m venv venv
    
    # Instale todas as dependências necessárias
    pip install -r requirements.txt
    
    3. Configure o Banco de Dados:
    
        Crie um arquivo chamado .env na pasta raiz do projeto.
    
        Dentro deste arquivo, adicione uma única linha com a sua URL de conexão do Neon:
    
        DATABASE_URL="sua_url_de_conexao_do_neon_aqui"
    
    4. Execute a Aplicação:
    
    python app.py
    
    5. Acesse no Navegador:
    
        Após executar o comando, o servidor estará rodando.
    
        Abra seu navegador de internet e acesse o seguinte endereço: http://127.0.0.1:5000
    
        A interface da agenda de contatos será exibida.

## Autores

    [João Victor Souza Cruz]

    [Marcus Vinícius Braz Garcia]

    [Felipe Oliveira Cunha]

    [Gabriell Pereira Pinto Guedes]
