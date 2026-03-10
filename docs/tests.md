# Guia de Testes Automatizados

##  Visão Geral

Este projeto utiliza **pytest** para testes automatizados, com suporte a:
- Testes unitários
- Testes de integração
- Cobertura de código
- Testes em container Docker
- Fixtures compartilhadas

##  Executando os Testes

### Pré-requisitos

- Python 3.12+
- Docker (opcional, para testes em container)
- Dependências instaladas: `pip install -r requirements.txt`

### Comandos Básicos

```bash
# Executar todos os testes
pytest

# Executar com mais detalhes
pytest -v

# Executar testes específicos
pytest tests/unit/                  # apenas unitários
pytest tests/integration/            # apenas integração
pytest tests/test_health.py          # arquivo específico

# Executar testes por marcador
pytest -m unit                        # apenas testes unitários
pytest -m integration                 # apenas testes de integração

# Executar com cobertura
pytest --cov=app tests/               # mostra cobertura no terminal
pytest --cov=app --cov-report=html    # gera relatório HTML
```
### Testes com Docker

``` bash

# Usando docker-compose específico para testes
docker-compose -f docker-compose.test.yml up --build

# Ou usando o script helper
./scripts/run_tests.sh --docker

# Executar comando personalizado no container
docker-compose -f docker-compose.test.yml run --rm test pytest tests/unit -v
```