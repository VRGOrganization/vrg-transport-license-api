from fastapi import APIRouter, Query
from fastapi.responses import Response

from app.schemas.output_format import MEDIA_TYPES, OutputFormat
from app.schemas.student import Student
from app.services.fill_license import fill_license

router = APIRouter(prefix="/license")


@router.get("")
def license_check():
    return {"status": "OK"}


@router.post("/create")
def create_license(
    student: Student,
    output_format: OutputFormat = Query(default=OutputFormat.JPG, alias="format"),
) -> Response:
    content: bytes = fill_license(student, output_format)
    return Response(content=content, media_type=MEDIA_TYPES[output_format])