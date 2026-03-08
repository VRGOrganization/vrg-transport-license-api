# VRG Transport API License

    API de licenciamento VRG. Sistema responsável pelo gerenciamento de licenças de estudantes universitários e transporte intermunicipal.

## Sobre o Projeto

    A VRG Transport API License é uma solução desenvolvida para automatizar e gerenciar o processo de criação de carteirinhas estudantis municipais. A API oferece endpoints para criação, validação e monitoramento de licenças, garantindo conformidade na criação das carteirinhas. 

###  Objetivos

    - Criação de carteirinhas estudantis em .png. 
    - Api será conectada a uma segunda API.
## Tecnologias

- **Python 3.12+** - Linguagem base
- **FastAPI** - Framework web assíncrono
- **Uvicorn** - Servidor ASGI de alta performance
- **Docker** - Containerização da aplicação
- **Docker Compose** - Orquestração de containers
- **Pydantic** - Validação de dados e serialização
- **Pytest** - Testes automatizados

## Estrutura do Projeto

Estrutura do projeto 

|--> app
| |--> models
| | |--> __init_.py
| |--> routes
| | |--> __init_.py
| | |--> health.py
| |--> schema 
| | |--> __init_.py
| |--> service
| | |--> __init_.py
| |-->  __init_.py
| |-->  main.py
|-->  .dockerignore
|--> .env.exemple
|--> .gitignore
|--> docker-compose.yml
|--> dockerfile

## Configuração do Ambiente 

[ Configure o projeto ](./configInit.md)

## Inicializar Projeto

[ Inicie o projeto na sua máquina ](InitProject.md)

## Padrões de commits

[ Verifique os padrões de commit que estão sendo utilizados nesse projeto](commits.md)

## Fluxo de Branches

    Toda branch de desenvolvimento deverá vir da branch dev para que sigas as diretrizes da empresa.

## Endpoints 

    (POST) /api/v1.0/license/create 
        -> return 200 ok
        -> return 404 not found
        -> return 422 
        
## Schema 

    Studant 
        -> id: string 
        -> bane: string
        -> registry: string
        -> institution: string
        -> shift: string 
        -> telephone: string
        -> blood_type: string

## Contribuição

    Por favor, leia os documentos de [ padrões de commit ](commits.md) e [ Fluxo de Branches](#fluxo-de-branches) antes de contribuir.

## Licença

    Este projeto é proprietário e confidencial. Todos os direitos reservados.