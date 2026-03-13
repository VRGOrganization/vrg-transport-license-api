import base64
import binascii
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from PIL.Image import UnidentifiedImageError

from app.config import FIELD_FONT_SIZES, FIELD_POSITIONS, FONT_PATHS, PHOTO_POSITION, PHOTO_SIZE, TEMPLATE_PATH, TEXT_COLOR
from app.errors import AppError
from app.schemas.student import Student

"""
Procura uma fonte em ./app/assets/fonts
Nao tem problema se der continue no OSError pois ele vai retornar uma default
"""
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
    try:
        photo_bytes = base64.b64decode(photo_base64)
    except (binascii.Error, ValueError) as e:
        raise AppError(
            code="ERR002",
            origin="service.fill_license.photo_base64",
            context={"error": str(e)},
        )
    
    try:
        photo = Image.open(BytesIO(photo_bytes)).convert("RGB")
    except UnidentifiedImageError as e:
        raise AppError(
            code="ERR003",
            origin="service.fill_license.photo_format",
            context={"error": str(e)},
        )
    except Exception as e:
        raise AppError(
            code="ERR004",
            origin="service.fill_license.photo_processing",
            context={"error": str(e)},
        )
    
    photo = photo.resize(PHOTO_SIZE)
    template.paste(photo, PHOTO_POSITION)

# Exporta a imagem como JPEG e retorna os bytes.
#TODO: retornar em PNG com uma qualidade boa
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
    try:
        template: Image.Image = Image.open(TEMPLATE_PATH).convert("RGB")
    except FileNotFoundError:
        raise AppError(
            code="ERR010", 
            origin="service.fill_license.template_not_found"
        )
    except UnidentifiedImageError:
        raise AppError(
            code="ERR011", 
            origin="service.fill_license.template_invalid"
        )
    except Exception as e:
        raise AppError(
            code="ERR012",
            origin="service.fill_license.template_load",
            context={"error": str(e)},
        )
    
    if student.photo:
        _paste_photo(template, student.photo)

    _write_fields(ImageDraw.Draw(template), student)

    return _export_image(template)