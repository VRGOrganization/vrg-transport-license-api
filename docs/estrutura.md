# Estrutura do Projeto

```
app/
  main.py              -- Inicializacao do FastAPI, registro de rotas
  config.py            -- Caminhos de assets, posicoes dos campos, fontes, cores
  assets/
    license_template.jpg  -- Template base da carteirinha
    fonts/
      Roboto-Regular.ttf  -- Fonte usada na renderizacao
  models/               -- (reservado para modelos de banco futuros)
  routes/
    health.py           -- GET /health
    license.py          -- GET /license, POST /license/create
  schemas/
    student.py          -- Schema Pydantic do estudante
    output_format.py    -- Enum de formato (jpg/pdf) e mapa de media types
  services/
    fill_license.py     -- Logica de geracao da carteirinha (renderizacao + exportacao)
```

## Fluxo da geracao

1. `POST /license/create` recebe os dados do estudante
2. `fill_license()` abre o template, escreve os campos nas posicoes definidas em `config.py`
3. A imagem e exportada no formato escolhido (JPG ou PDF)
4. Os bytes sao retornados diretamente na resposta HTTP
