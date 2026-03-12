# Testes Automatizados

Suite de testes usando pytest para validar a API de geracao de carteirinhas.

**Total: 29 testes | 100% de cobertura de codigo**

## Estrutura

```
tests/
├── conftest.py                    # Fixtures compartilhadas
├── test_routes_license.py         # 9 testes da rota /license/create
├── test_routes_health.py          # 3 testes da rota /health
├── test_schemas_student.py        # 8 testes do schema Pydantic
└── test_services_fill_license.py  # 9 testes do servico de geracao
```

## Instalacao

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependencias (inclui pytest)
pip install -r requirements.txt
```

## Executar Testes

```bash
# Todos os testes
pytest

# Com verbosidade
pytest -v

# Testes especificos
pytest tests/test_routes_license.py -v
pytest tests/test_schemas_student.py -v

# Com cobertura
pytest --cov=app --cov-report=term

# Cobertura HTML
pytest --cov=app --cov-report=html
```

## O Que os Testes Validam

### Rota /license/create

**Autenticacao:**
- API key valida retorna 201
- API key invalida retorna 403
- API key ausente retorna 403
- API_KEY=None permite acesso sem autenticacao

**Validacao de Dados:**
- Dados validos com foto retorna 201 + imagem base64
- Dados validos sem foto retorna 201 + imagem base64
- Campo obrigatorio faltando retorna 422
- Campos com strings vazias retorna 422
- Tipo de dado invalido retorna 422
- Body vazio retorna 422

### Rota /health

- Retorna status 200
- Retorna string "healthy"
- Nao requer autenticacao

### Schema Student

- Aceita dados validos com/sem foto
- Rejeita campos obrigatorios faltantes
- Rejeita tipos de dados invalidos
- Rejeita strings vazias (min_length=1)
- Campo photo e opcional (None ou omitido)

### Servico fill_license

- Carrega fontes (com fallback para fonte padrao)
- Escreve campos na imagem
- Processa foto base64 (decodifica, redimensiona, cola)
- Rejeita base64 invalido
- Exporta imagem como bytes JPEG
- Gera carteirinha com/sem foto
- Trata template nao encontrado

## Fixtures Disponiveis

Definidas em `conftest.py`:

| Fixture | Descricao |
|---------|-----------|
| `test_client` | Cliente de teste FastAPI |
| `mock_api_key` | API key mockada para testes |
| `mock_api_key_none` | Desabilita autenticacao (API_KEY=None) |
| `valid_student_data` | Dados validos com foto |
| `valid_student_data_no_photo` | Dados validos sem foto |
| `empty_student_data` | Strings vazias (testa validacao) |
| `mock_fill_license` | Mock do servico de geracao |

## Cobertura de Codigo

```
Name                           Stmts   Miss  Cover
--------------------------------------------------
app/config.py                     13      0   100%
app/main.py                        5      0   100%
app/routes/health.py               5      0   100%
app/routes/license.py             15      0   100%
app/schemas/student.py            11      0   100%
app/services/fill_license.py      35      0   100%
--------------------------------------------------
TOTAL                             86      0   100%
```

## Comandos Uteis

```bash
# Rodar testes
pytest
pytest -v                                    # verbose
pytest -x                                    # parar no primeiro erro
pytest --lf                                  # apenas testes que falharam

# Cobertura
pytest --cov=app                             # basico
pytest --cov=app --cov-report=term-missing   # mostrar linhas faltando
pytest --cov=app --cov-report=html           # relatorio HTML
```

## Contribuindo

Ao adicionar funcionalidades:

1. Escreva testes primeiro (TDD)
2. Mantenha cobertura em 100%
3. Use fixtures do conftest.py
4. Execute testes antes de commitar
