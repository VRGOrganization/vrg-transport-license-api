# Configuração do Ambiente

## Pré-requisitos

- Python 3.12 ou superior
- Docker e Docker Compose 
- Git

## Instalação Local

1. **Clone o repositório**
   ```bash
   git clone git@github.com:VRGOrganization/vrg-transport-license-api.git
   cd vrg-transport-api-license

## Crie e ative um ambiente virtual

python -m venv venv
source venv/bin/activate  # Linux/Mac
ou
venv\Scripts\activate  # Windows

## Instale as dependências

pip install -r requirements.txt

## Configure as variáveis de ambiente

cp .env.example .env
-- > Edite as configurações 


## Execute a aplicação

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000