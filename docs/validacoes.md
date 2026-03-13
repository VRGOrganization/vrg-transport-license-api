# Validacoes da API

Documentacao das validacoes implementadas na API de geracao de carteirinhas.

## Schema Student

Todos os campos obrigatorios possuem validacao para garantir que nao sejam strings vazias.

### Implementacao

```python
from pydantic import BaseModel, Field

class Student(BaseModel):
    id: str = Field(min_length=1, description="ID do estudante")
    employee_id: str = Field(min_length=1, description="ID do funcionario que realizou criacao da carteirinha")
    name: str = Field(min_length=1, description="Nome completo do estudante")
    degree: str = Field(min_length=1, description="Curso do estudante")
    institution: str = Field(min_length=1, description="Instituicao de ensino")
    shift: str = Field(min_length=1, description="Turno (Manha, Tarde, Noite)")
    telephone: str = Field(min_length=1, description="Telefone de contato")
    blood_type: str = Field(min_length=1, description="Tipo sanguineo")
    bus: str = Field(min_length=1, description="Numero do onibus")
    photo: str | None = None  # base64 da foto do estudante (opcional)
```

### Regras de Validacao

| Campo | Tipo | Obrigatorio | Validacao |
|-------|------|-------------|-----------|
| `id` | string | Sim | min_length=1 |
| `employee_id` | string | Sim | min_length=1 |
| `name` | string | Sim | min_length=1 |
| `degree` | string | Sim | min_length=1 |
| `institution` | string | Sim | min_length=1 |
| `shift` | string | Sim | min_length=1 |
| `telephone` | string | Sim | min_length=1 |
| `blood_type` | string | Sim | min_length=1 |
| `bus` | string | Sim | min_length=1 |
| `photo` | string \| null | Nao | - |

## Exemplos

### Requisicao Valida

**Requisicao:**
```json
POST /api/v1/license/create
Headers: X-Api-Key: sua-chave

{
  "id": "2024001",
  "employee_id": "emp-0001",
  "name": "Joao da Silva",
  "degree": "Engenharia de Software",
  "institution": "UFPE",
  "shift": "Manha",
  "telephone": "(81) 99999-9999",
  "blood_type": "O+",
  "bus": "123",
  "photo": "base64_string..."
}
```

**Resposta:** `201 Created`
```json
{
  "image": "base64_da_carteirinha..."
}
```

### Campo Vazio

**Requisicao:**
```json
{
  "id": "2024001",
  "employee_id": "emp-0001",
  "name": "",  // String vazia
  ...
}
```

**Resposta:** `422 Unprocessable Entity`
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "name"],
      "msg": "String should have at least 1 character"
    }
  ]
}
```

### Campo Faltando

**Requisicao:**
```json
{
  "id": "2024001",
  "employee_id": "emp-0001",
  // "name": faltando
  ...
}
```

**Resposta:** `422 Unprocessable Entity`
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "name"],
      "msg": "Field required"
    }
  ]
}
```

### Tipo Incorreto

**Requisicao:**
```json
{
  "id": 2024001,  // Numero ao inves de string
  "employee_id": "emp-0001",
  ...
}
```

**Resposta:** `422 Unprocessable Entity`
```json
{
  "detail": [
    {
      "type": "string_type",
      "loc": ["body", "id"],
      "msg": "Input should be a valid string"
    }
  ]
}
```

## Autenticacao

A rota `/license/create` valida API key via header `X-Api-Key`:

```python
if API_KEY is not None and x_api_key != API_KEY:
  raise AppError(code="ERR001", origin="route.license.auth")
```

| Cenario | Resposta |
|---------|----------|
| API_KEY configurada + header correto | 201/422 |
| API_KEY configurada + header errado | 403 Forbidden |
| API_KEY configurada + sem header | 403 Forbidden |
| API_KEY nao configurada (None) | 201/422 (sem autenticacao) |

**Exemplo - Nao Autorizado:**

```bash
POST /api/v1/license/create
Headers: X-Api-Key: chave-errada
```

Resposta: `403 Forbidden`
```json
{
  "code": "ERR001",
  "status": 403
}
```

## Validacao Automatica

O FastAPI com Pydantic valida automaticamente:
- Antes da requisicao chegar no endpoint
- Erros detalhados com localizacao exata
- Multiplos erros retornados de uma vez
- Documentacao automatica no Swagger

**Swagger UI:** `http://localhost:8000/docs`

## Testando Validacoes

```bash
# Testes do schema
pytest tests/test_schemas_student.py -v

# Testes da rota
pytest tests/test_routes_license.py -v
```

Ver [testes.md](./testes.md) para detalhes.

## Historico

### 2026-03-12: Validacao de Strings Vazias

**Implementado:** `Field(min_length=1)` em todos os campos obrigatorios

**Antes:**
```python
name: str  # Aceitava ""
```

**Depois:**
```python
name: str = Field(min_length=1)  # Rejeita ""
```

**Impacto:** Strings vazias agora retornam 422
