# Configuracao

## Template

O template da carteirinha fica em `app/assets/license_template.jpg`. Para trocar, substitua o arquivo mantendo o mesmo nome.

## Posicoes dos campos

Definidas em `app/config.py` no dicionario `FIELD_POSITIONS`. Cada campo mapeia para uma coordenada `(x, y)` em pixels:

```python
FIELD_POSITIONS = {
    "name": (300, 50),
    "degree": (300, 100),
    "registry": (300, 150),
    "institution": (300, 200),
    "shift": (300, 250),
    "telephone": (300, 300),
    "blood_type": (300, 350),
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
