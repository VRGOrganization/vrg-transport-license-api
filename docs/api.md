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

Gera a carteirinha do estudante a partir dos dados enviados. Retorna a imagem em base64 no corpo da resposta.

**Headers:**

| Header      | Tipo   | Obrigatorio | Descricao                          |
|-------------|--------|-------------|------------------------------------|
| `X-Api-Key` | string | Sim*        | Chave de autorizacao da API        |

\* Obrigatorio quando a chave estiver configurada no servidor.

**Body (JSON):**

```json
{
  "id": "1",
  "name": "Joao da Silva",
  "degree": "Engenharia de Software",
  "institution": "UFPE",
  "shift": "Manha",
  "telephone": "(81) 99999-0000",
  "blood_type": "O+",
  "photo": "<base64 da foto do estudante (opcional)>"
}
```

**Campos obrigatorios:** todos, exceto `photo`.

**Respostas:**

| Status | Descricao                          |
|--------|------------------------------------|
| 201    | Carteirinha gerada com sucesso     |
| 403    | Nao autorizado (chave invalida)    |
| 422    | Campos obrigatorios ausentes       |

**Resposta 201:**

```json
{
  "image": "<base64 da imagem JPG>"
}
```

**Exemplo com curl:**

```bash
curl -s -X POST http://localhost:8000/api/v1/license/create \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: SUA_CHAVE" \
  -d '{
    "id": "1",
    "name": "Joao da Silva",
    "degree": "Engenharia de Software",
    "institution": "UFPE",
    "shift": "Manha",
    "telephone": "(81) 99999-0000",
    "blood_type": "O+"
  }'
```
