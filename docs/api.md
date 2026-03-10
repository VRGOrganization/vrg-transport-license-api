# API

Base URL: `http://localhost:8000`

Root path: `/api/v1`

## Endpoints

### GET /health

Verifica se a API esta rodando.

**Resposta:**

```json
{"status": "healthy"}
```

### GET /license

Verifica se o modulo de licenca esta ativo.

**Resposta:**

```json
{"status": "OK"}
```

### POST /license/create

Gera a carteirinha do estudante a partir dos dados enviados. Retorna a imagem diretamente no body da resposta (nao salva em disco).

**Body (JSON):**

```json
{
  "id": "1",
  "name": "Joao da Silva",
  "degree": "Engenharia de Software",
  "registry": "2024001",
  "institution": "UFPE",
  "shift": "Manha",
  "telephone": "(81) 99999-0000",
  "blood_type": "O+"
}
```

**Campos obrigatorios:** todos.

**Resposta:** `image/jpeg`

**Exemplo com curl:**

```bash
mkdir -p tmp
curl -s -o tmp/carteirinha.jpg -X POST http://localhost:8000/license/create \
  -H "Content-Type: application/json" \
  -d '{
    "id": "1",
    "name": "Joao da Silva",
    "degree": "Engenharia de Software",
    "registry": "2024001",
    "institution": "UFPE",
    "shift": "Manha",
    "telephone": "(81) 99999-0000",
    "blood_type": "O+"
  }'
```
