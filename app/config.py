import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ASSETS_DIR: Path = Path(__file__).resolve().parent / "assets"
TEMPLATE_PATH: Path = ASSETS_DIR / "modelo.jpg"

FIELD_POSITIONS: dict[str, tuple[int, int]] = {
    "name":        (280,  70),   # campo Nome
    "institution": (280, 145),   # campo Inst.
    "degree":      (280, 210),   # campo Curso
    "telephone":   (280, 285),   # campo Cel.
    "shift":       (280, 355),   # campo Período
    "blood_type":  (520, 355),   # campo Tipo Sanguíneo
}

TEXT_COLOR: tuple[int, int, int] = (0, 0, 0)
FONT_SIZE: int = 20

FONT_PATHS: list[str] = [
    str(ASSETS_DIR / "font.ttf"),
    "app/assets/fonts/Roboto-Regular.ttf"
]

API_KEY: str | None = os.getenv("API_KEY")
