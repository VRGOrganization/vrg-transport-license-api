# VRG Transport API License

API de licenciamento para transporte VRG.

## Requisitos

- Python 3.12+
- Docker (opcional)

## Executar localmente

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Executar com Docker

```bash
cp .env.example .env
docker compose up --build
```

## Endpoints

| Método | Rota      | Descrição    |
|--------|-----------|--------------|
| GET    | `/health` | Health check |

## Acesso

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
