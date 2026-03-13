# Configuracao

## Template

O template da carteirinha fica em `app/assets/modelo.jpg`. Para trocar, substitua o arquivo mantendo o mesmo nome.

## Posicoes dos campos

Definidas em `app/config.py` no dicionario `FIELD_POSITIONS`. Cada campo mapeia para uma coordenada `(x, y)` em pixels:

```python
FIELD_POSITIONS = {
    "name":        (280,  70),
    "institution": (280, 145),
    "degree":      (280, 210),
    "telephone":   (280, 285),
    "shift":       (280, 355),
    "blood_type":  (520, 355),
}
```

Ajuste os valores conforme o layout do template.

## Fonte

A fonte e carregada na seguinte ordem de prioridade:

1. `app/assets/font.ttf` (fonte customizada, se existir)
2. `app/assets/fonts/Roboto-Regular.ttf` (fonte padrao incluida)

Para trocar a fonte, coloque o arquivo `.ttf` desejado e atualize os caminhos em `FONT_PATHS` no `app/config.py`.

Tamanho padrao: 20px (variavel `FONT_SIZE`).

## Cor do texto

Definida em `TEXT_COLOR` como tupla RGB. Padrao: `(0, 0, 0)` (preto).

## Docker

Requer um arquivo `.env` na raiz (mesmo que vazio). O container expoe a porta 8000.

Variaveis recomendadas para logs no Mongo Atlas:

```env
APP_ENV=development
API_KEY=teste-123
MONGO_URI=mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/?retryWrites=true&w=majority&appName=<app-name>
MONGO_DB=vrg_transport
MONGO_COLLECTION=operation_logs
```

```bash
# subir
docker compose up -d --build

# rebuild sem cache
docker compose build --no-cache && docker compose up -d

# ver logs
docker compose logs -f api
```

## Dependencias

- Python 3.12+
- fastapi >= 0.104.0
- uvicorn[standard] >= 0.24.0
- Pillow >= 10.0.0
- python-dotenv >= 1.0.0
- pymongo >= 4.8.0
