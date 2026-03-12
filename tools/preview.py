"""Visualiza a carteirinha a partir do retorno base64 da API.

Uso:
    python tools/preview.py '<json_response>'
    python tools/preview.py '{"image": "/9j/4AAQ..."}'

    # Ou direto do curl:
    curl -s -X POST http://localhost:8000/api/v1/license/create \
      -H "Content-Type: application/json" \
      -H "X-Api-Key: SUA_CHAVE" \
      -d '{ ... }' | python tools/preview.py

A imagem e salva em tmp/preview.jpg e aberta automaticamente (se possivel).
"""

import base64
import json
import sys
from pathlib import Path


def preview(response_json: str) -> None:
    data = json.loads(response_json)
    image_b64 = data.get("image")

    if not image_b64:
        print("Erro: campo 'image' nao encontrado no JSON.")
        sys.exit(1)

    image_bytes = base64.b64decode(image_b64)

    output_dir = Path(__file__).resolve().parent.parent / "tmp"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "preview.jpg"

    output_path.write_bytes(image_bytes)
    print(f"Carteirinha salva em: {output_path}")


if __name__ == "__main__":
    if not sys.stdin.isatty():
        raw = sys.stdin.read()
    elif len(sys.argv) > 1:
        raw = sys.argv[1]
    else:
        print("Uso: python tools/preview.py '<json>' ou pipe do curl")
        sys.exit(1)

    preview(raw)
