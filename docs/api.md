# API

Base URL: `http://localhost:8000`

Root path: `/api/v1`

## Endpoints

### GET /health

Verifica se a API esta rodando.

**Resposta:** `200 OK`

```json
"healthy"
```

### POST /license/create

Gera a carteirinha do estudante a partir dos dados enviados. Retorna a imagem em base64.

**Headers:**

| Header      | Tipo   | Obrigatorio | Descricao                          |
|-------------|--------|-------------|------------------------------------|
| `X-Api-Key` | string | Condicional | Chave de autorizacao da API        |

*Obrigatorio apenas quando API_KEY estiver configurada no servidor.

**Body (JSON):**

```json
{
  "id": "1",
  "employee_id": "emp-0001",
  "name": "Joao da Silva",
  "degree": "Engenharia de Software",
  "institution": "UFPE",
  "shift": "Manha",
  "telephone": "(81) 99999-0000",
  "blood_type": "O+",
  "bus": "02",
  "photo": "<base64 da foto do estudante (opcional)>"
}
```

**Campos obrigatorios:** Todos exceto `photo`

**Validacoes:**
- Todos os campos obrigatorios devem ter pelo menos 1 caractere
- Strings vazias sao rejeitadas
- `photo` e opcional (pode ser null ou omitido)

**Respostas:**

| Status | Descricao                                    |
|--------|----------------------------------------------|
| 201    | Carteirinha gerada com sucesso               |
| 403    | Nao autorizado (chave invalida ou ausente)   |
| 400    | Erro de entrada (foto/base64/imagem)         |
| 500    | Erro interno no processamento                |
| 422    | Dados invalidos (campo faltando ou vazio)    |

**Resposta 201:**

```json
{
  "image": "<base64 da imagem JPG>"
}
```

**Contrato de erro (catalogo):**

Para erros controlados da aplicacao, a API retorna somente `code` e `status`.

```json
{
  "code": "ERR001",
  "status": 403
}
```

**Catalogo de codigos:**

| Code   | Status | Cenario |
|--------|--------|---------|
| ERR001 | 403    | Nao autorizado (API key invalida/ausente) |
| ERR002 | 400    | Foto em base64 invalida |
| ERR003 | 400    | Formato de imagem nao suportado |
| ERR004 | 400    | Erro ao processar foto |
| ERR010 | 500    | Template da carteirinha nao encontrado |
| ERR011 | 500    | Template da carteirinha invalido |
| ERR012 | 500    | Erro ao carregar template |
| ERR099 | 500    | Erro interno inesperado |

Observacao: erros de validacao de schema (Pydantic/FastAPI) continuam em `422` no formato padrao (`detail`).

**Exemplo com curl:**

```bash
curl -s -X POST http://localhost:8000/api/v1/license/create \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: SUA_CHAVE" \
  -d '{
    "id": "1",
    "employee_id": "emp-0001",
    "name": "Joao da Silva",
    "degree": "Engenharia de Software",
    "institution": "UFPE",
    "shift": "Manha",
    "telephone": "(81) 99999-0000",
    "blood_type": "O+",
    "bus": "02"
  }'
```
