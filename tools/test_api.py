"""Ferramenta interativa para testar o endpoint POST /license/create.

Uso:
    python3 tools/test_api.py
    python3 tools/test_api.py --url http://localhost:8000/api/v1
"""

import base64
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

BASE_URL = "http://localhost:8000/api/v1"
API_KEY = "test-key-123"

STUDENT_OK = {
    "id": "1",
    "name": "Joao da Silva",
    "degree": "Engenharia de Software",
    "institution": "UFPE",
    "shift": "Manha",
    "telephone": "(81) 99999-0000",
    "blood_type": "O+",
}

TESTS = {
    "1": {
        "label": "201 - Sucesso (sem foto)",
        "body": {**STUDENT_OK},
        "headers": {"X-Api-Key": API_KEY},
    },
    "2": {
        "label": "201 - Sucesso (com foto)",
        "body": {**STUDENT_OK},
        "headers": {"X-Api-Key": API_KEY},
        "ask_photo": True,
    },
    "3": {
        "label": "403 - Sem chave de autorizacao",
        "body": {**STUDENT_OK},
        "headers": {},
    },
    "4": {
        "label": "403 - Chave errada",
        "body": {**STUDENT_OK},
        "headers": {"X-Api-Key": "chave-errada"},
    },
    "5": {
        "label": "422 - Campos faltando (so id e name)",
        "body": {"id": "1", "name": "Joao"},
        "headers": {"X-Api-Key": API_KEY},
    },
    "6": {
        "label": "422 - Body vazio",
        "body": {},
        "headers": {"X-Api-Key": API_KEY},
    },
}

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "tmp"


def _image_to_base64(path: str) -> str:
    image_path = Path(path).expanduser().resolve()
    if not image_path.exists():
        print(f"  Arquivo nao encontrado: {image_path}")
        sys.exit(1)
    return base64.b64encode(image_path.read_bytes()).decode("utf-8")


def _do_request(body: dict, headers: dict) -> None:
    url = f"{BASE_URL}/license/create"
    headers["Content-Type"] = "application/json"
    payload = json.dumps(body).encode()

    req = urllib.request.Request(url, data=payload, headers=headers)

    try:
        resp = urllib.request.urlopen(req)
        status = resp.status
        data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        status = e.code
        data = json.loads(e.read())

    print(f"\n  HTTP {status}")
    if status == 201 and "image" in data:
        OUTPUT_DIR.mkdir(exist_ok=True)
        output_path = OUTPUT_DIR / "test_result.jpg"
        image_bytes = base64.b64decode(data["image"])
        output_path.write_bytes(image_bytes)
        print(f"  Carteirinha salva em: {output_path}")
    else:
        print(f"  Resposta: {json.dumps(data, indent=2, ensure_ascii=False)}")


def _show_menu() -> None:
    print("\n=== Testes do POST /license/create ===\n")
    for key, test in TESTS.items():
        print(f"  [{key}] {test['label']}")
    print(f"\n  [0] Sair")


def main() -> None:
    if "--url" in sys.argv:
        global BASE_URL
        idx = sys.argv.index("--url")
        BASE_URL = sys.argv[idx + 1]

    while True:
        _show_menu()
        choice = input("\nEscolha o teste: ").strip()

        if choice == "0":
            print("Saindo.")
            break

        test = TESTS.get(choice)
        if not test:
            print("  Opcao invalida.")
            continue

        print(f"\n> {test['label']}")
        body = dict(test["body"])

        if test.get("ask_photo"):
            photo_path = input("  Caminho da imagem: ").strip()
            if photo_path:
                body["photo"] = _image_to_base64(photo_path)
            else:
                print("  Nenhum caminho informado, enviando sem foto.")

        _do_request(body, dict(test["headers"]))


if __name__ == "__main__":
    main()
