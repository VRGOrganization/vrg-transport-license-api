from enum import Enum


class OutputFormat(str, Enum):
    JPG = "jpg"
    PDF = "pdf"


MEDIA_TYPES: dict[OutputFormat, str] = {
    OutputFormat.JPG: "image/jpeg",
    OutputFormat.PDF: "application/pdf",
}
