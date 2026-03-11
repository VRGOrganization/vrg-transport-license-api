from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from app.config import FIELD_FONT_SIZES, FIELD_POSITIONS, FONT_PATHS, PHOTO_POSITION, PHOTO_SIZE, TEMPLATE_PATH, TEXT_COLOR
from app.schemas.student import Student


def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _write_fields(draw: ImageDraw.ImageDraw, student: Student) -> None:
    fields: dict[str, str] = {
        "name": student.name,
        "institution": student.institution,
        "degree": student.degree,
        "telephone": student.telephone,
        "shift": student.shift,
        "blood_type": student.blood_type,
        "bus": student.bus
    }
    fonts = {field: _load_font(size) for field, size in FIELD_FONT_SIZES.items()}
    default_font = fonts["_default"]
    for field, value in fields.items():
        draw.text(FIELD_POSITIONS[field], value, fill=TEXT_COLOR, font=fonts.get(field, default_font))

# Decodifica a foto base64 e cola no template na posicao configurada
def _paste_photo(template: Image.Image, photo_base64: str) -> None:
    import base64
    photo_bytes = base64.b64decode(photo_base64)
    photo = Image.open(BytesIO(photo_bytes)).convert("RGB")
    photo = photo.resize(PHOTO_SIZE)
    template.paste(photo, PHOTO_POSITION)

# Exporta a imagem como JPEG e retorna os bytes.
def _export_image(image: Image.Image) -> bytes:
    buffer: BytesIO = BytesIO()
    image.save(buffer, "JPEG", quality=95)
    buffer.seek(0)
    return buffer.getvalue()

"""
Gera a carteirinha preenchida com os dados do estudante.
Abre o template, escreve os campos e exporta como JPEG.
"""
def fill_license(student: Student) -> bytes:
    template: Image.Image = Image.open(TEMPLATE_PATH).convert("RGB")
    if student.photo:
        _paste_photo(template, student.photo)

    _write_fields(ImageDraw.Draw(template), student)

    return _export_image(template)