# VRG Transport API License

API para geracao de carteirinhas de transporte estudantil.

## Rodar

```bash
docker compose up -d --build
```

API disponivel em `http://localhost:8000`.

## Documentacao

### API e Estrutura

- [API - Endpoints e exemplos](docs/api.md)
- [Estrutura do projeto](docs/estrutura.md)
- [Configuracao - Template, fontes, Docker](docs/configuracao.md)

### Desenvolvimento

- [Testes - Suite completa com pytest](docs/testes.md)
- [Validacoes - Schema e autenticacao](docs/validacoes.md)
- [Padrao de commits](docs/padrao-commits.md)

## Ferramentas

- [Preview da carteirinha](tools/docs/preview.md)
- [Teste interativo da API](tools/docs/test_api.md)
- [Mapeador de campos](tools/docs/map_fields.md)

## Testes

Execute a suite completa de testes:

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Rodar todos os testes
pytest

# Com cobertura de codigo
pytest --cov=app
```

**29 testes | 100% de cobertura**

Veja a [documentacao completa de testes](docs/testes.md) para mais detalhes.
