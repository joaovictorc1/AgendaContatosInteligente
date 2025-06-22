Projeto Integrador: Agenda de Contatos com Login

Este projeto é uma agenda de contatos desenvolvida em Python, utilizando a biblioteca Tkinter para a interface gráfica, um banco de dados PostgreSQL (hospedado no Neon) para persistência de dados e um sistema de autenticação de usuários.

O projeto foi criado para a disciplina de Estrutura de Dados e, portanto, também inclui uma implementação de lista encadeada como parte dos requisitos acadêmicos.
Funcionalidades

    Sistema de Login:

        Registro de novos usuários.

        Login seguro com senha criptografada (bcrypt).

        Alteração de senha para o usuário logado.

        Logout.

    Gerenciamento de Contatos:

        Adicionar, editar e remover contatos.

        Listar todos os contatos em ordem alfabética.

        Buscar contatos por nome ou telefone.

    Persistência de Dados:

        Todas as informações de usuários e contatos são armazenadas em um banco de dados PostgreSQL.

Estrutura do Projeto

    main.py: Ponto de entrada da aplicação. Contém o código da interface gráfica (Login e Agenda).

    database.py: Gerencia a conexão com o banco de dados PostgreSQL (Neon).

    auth.py: Módulo responsável pela autenticação e gerenciamento de usuários.

    crud_contatos.py: Módulo com as operações de CRUD (Create, Read, Update, Delete) para os contatos.

    estruturas.py: Módulo com a implementação da estrutura de dados (lista encadeada).

    .env: Arquivo local (não versionado) para armazenar as credenciais do banco de dados.

Como Executar

    Pré-requisitos:

        Python 3.6 ou superior.

        Uma conta no Neon com um projeto de banco de dados criado.

    Instalação de Dependências:

    pip install psycopg2-binary bcrypt python-dotenv

    Configuração do Ambiente:

        Crie um arquivo chamado .env na pasta raiz do projeto.

        Abra seu projeto no Neon, vá para a seção "Connection Details" e copie a URL de conexão (Connection String).

        Cole a URL de conexão dentro do arquivo .env, como no exemplo abaixo:

    DATABASE_URL="postgres://user:password@host:port/dbname"

    Execução:

        Com o arquivo .env configurado e as dependências instaladas, execute o arquivo principal:

    python main.py

        A tela de login será exibida. Você pode registrar um novo usuário e depois fazer o login para acessar a agenda.