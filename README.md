Projeto Integrador: Agenda de Contatos Web

Este projeto é uma agenda de contatos desenvolvida como uma aplicação web moderna utilizando Python com o framework Flask. Ele cumpre os requisitos da disciplina de Estrutura de Dados, implementando um backend robusto com sistema de login e persistência de dados em um banco de dados local SQLite.
Funcionalidades

    Interface Web Moderna: Interface de usuário limpa e responsiva, acessível por qualquer navegador web.

    Sistema de Login Seguro:

        Registro de novos usuários.

        Login com senha criptografada (utilizando bcrypt).

        Gerenciamento de sessão de usuário.

    Gerenciamento de Contatos (CRUD):

        Adicionar, editar e remover contatos em tempo real.

        Listagem e busca de contatos.

    Banco de Dados Local: Utiliza SQLite para uma persistência de dados simples e confiável, que funciona em qualquer máquina sem necessidade de configuração externa.

Estrutura do Projeto

    app.py: O coração da aplicação. Contém o servidor web Flask e todas as rotas da API. É este o arquivo que deve ser executado.

    database.py: Módulo que gerencia a criação do banco de dados SQLite e das tabelas.

    auth.py: Módulo responsável pela lógica de autenticação e gerenciamento de usuários.

    crud_contatos.py: Módulo com as funções para manipular os dados dos contatos no banco.

    estruturas.py: Contém a implementação da estrutura de dados (lista encadeada), como requisito acadêmico.

    templates/index.html: Arquivo HTML que contém toda a estrutura visual da aplicação.

    requirements.txt: Lista as dependências Python do projeto.

Como Executar

    Pré-requisitos:

        Python 3.6 ou superior.

    Clone o Repositório:

    git clone https://github.com/seu-usuario/nome-do-projeto.git
    cd nome-do-projeto

    Instale as Dependências:

        É altamente recomendado criar um ambiente virtual:

        python -m venv venv
        source venv/bin/activate  # No Windows: venv\Scripts\activate

        Instale as bibliotecas necessárias:

        pip install -r requirements.txt

    Execute a Aplicação:

    python app.py

    Acesse no Navegador:

        Após executar o comando acima, o servidor estará rodando.

        Abra seu navegador de internet e acesse o seguinte endereço: http://127.0.0.1:5000

        A interface da agenda de contatos será exibida.