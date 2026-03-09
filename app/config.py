from pathlib import Path

ASSETS_DIR: Path = Path(__file__).resolve().parent / "assets"
TEMPLATE_PATH: Path = ASSETS_DIR / "license_template.jpg"

FIELD_POSITIONS: dict[str, tuple[int, int]] = {
    "name": (300, 50),
    "degree": (300, 100),
    "registry": (300, 150),
    "institution": (300, 200),
    "shift": (300, 250),
    "telephone": (300, 300),
    "blood_type": (300, 350),
}

TEXT_COLOR: tuple[int, int, int] = (0, 0, 0)
FONT_SIZE: int = 20

FONT_PATHS: list[str] = [
    str(ASSETS_DIR / "font.ttf"),
    "app/assets/fonts/Roboto-Regular.ttf"
]
