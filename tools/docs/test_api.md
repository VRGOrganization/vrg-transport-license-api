# Teste Interativo da API

Ferramenta interativa para testar o endpoint `POST /license/create` com cenarios de sucesso e erro.

## Requisitos

- Python 3.10+
- API rodando (local ou Docker)
- Nenhuma dependencia externa

## Uso

```bash
python3 tools/test_api.py
```

Para apontar pra outro servidor:

```bash
python3 tools/test_api.py --url http://outro:8000/api/v1
```

## Menu

```
=== Testes do POST /license/create ===

  [1] 201 - Sucesso (sem foto)
  [2] 201 - Sucesso (com foto)
  [3] 403 - Sem chave de autorizacao
  [4] 403 - Chave errada
  [5] 422 - Campos faltando (so id e name)
  [6] 422 - Body vazio

  [0] Sair
```

## Teste com foto

Na opcao **[2]**, o script pede o caminho da imagem:

```
Caminho da imagem: /home/usuario/foto.jpg
```

Aceita caminho absoluto, relativo ou com `~/`. O arquivo e convertido automaticamente para base64 e enviado no campo `photo`.

Formatos aceitos: JPG, PNG ou qualquer formato suportado pelo Pillow.

## Saida

- Se **201**: salva a carteirinha em `tmp/test_result.jpg`
- Se **erro**: exibe o JSON de resposta no terminal
