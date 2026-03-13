# Preview da Carteirinha

Ferramenta para visualizar a carteirinha gerada pela API a partir do retorno base64.

## Requisitos

- Python 3.10+
- Nenhuma dependencia externa

## Uso

### Via pipe do curl

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
  }' | python3 tools/preview.py
```

### Passando o JSON como argumento

```bash
python3 tools/preview.py '{"image": "/9j/4AAQ..."}'
```

## Saida

A imagem e salva em `tmp/preview.jpg` na raiz do projeto.

```
Carteirinha salva em: /caminho/do/projeto/tmp/preview.jpg
```

## Observacoes

- O script aceita o JSON completo retornado pela API (campo `image` com base64).
- Totalmente desacoplado da API — usa apenas bibliotecas padrao do Python.
- A pasta `tmp/` e criada automaticamente se nao existir.
