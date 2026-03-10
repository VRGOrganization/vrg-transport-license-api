from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from app.config import FIELD_POSITIONS, FONT_PATHS, FONT_SIZE, TEMPLATE_PATH, TEXT_COLOR
from app.schemas.output_format import OutputFormat
from app.schemas.student import Student


def _load_font(size: int = FONT_SIZE) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _write_fields(draw: ImageDraw.ImageDraw, student: Student, font: ImageFont.FreeTypeFont | ImageFont.ImageFont) -> None:
    fields: dict[str, str] = {
        "name": student.name,
        "institution": student.institution,
        "degree": student.degree,
        "telephone": student.telephone,
        "shift": student.shift,
        "blood_type": student.blood_type,
    }
    for field, value in fields.items():
        draw.text(FIELD_POSITIONS[field], value, fill=TEXT_COLOR, font=font)


def _export_image(image: Image.Image, output_format: OutputFormat) -> bytes:
    buffer: BytesIO = BytesIO()
    if output_format == OutputFormat.PDF:
        image.save(buffer, "PDF")
    else:
        image.save(buffer, "JPEG", quality=95)
    buffer.seek(0)
    return buffer.getvalue()


def fill_license(student: Student, output_format: OutputFormat = OutputFormat.JPG) -> bytes:
    template: Image.Image = Image.open(TEMPLATE_PATH).convert("RGB")
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont = _load_font()

    _write_fields(ImageDraw.Draw(template), student, font)

    return _export_image(template, output_format)