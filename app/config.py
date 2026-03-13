import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ASSETS_DIR: Path = Path(__file__).resolve().parent / "assets"
TEMPLATE_PATH: Path = ASSETS_DIR / "modelo_carteirinha.png"

FIELD_POSITIONS: dict[str, tuple[int, int]] = {
    "name":        (340,  80),   # campo Nome
    "institution": (340, 167),   # campo Inst.
    "degree":      (340, 257),   # campo Curso
    "telephone":   (340, 346),   # campo Cel.
    "shift":       (340, 435),   # campo Período
    "blood_type":  (640, 435),  # campo Tipo Sanguíneo
    "bus":         (590, 555),   # campo Onibus
}

PHOTO_POSITION: tuple[int, int] = (42, 92)    # (x, y) onde a foto sera colada
PHOTO_SIZE: tuple[int, int] = (200, 250)      # (largura, altura) da foto em pixels

TEXT_COLOR: tuple[int, int, int] = (0, 0, 0)

FIELD_FONT_SIZES: dict[str, int] = {
    "_default": 20,
    "bus": 40,
}

FONT_PATHS: list[str] = [
    str(ASSETS_DIR / "font.ttf"),
    "app/assets/fonts/Roboto-Regular.ttf"
]

API_KEY: str | None = os.getenv("API_KEY")
