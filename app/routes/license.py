from fastapi import APIRouter
from fastapi.responses import Response

from app.schemas.student import Student
from app.services.fill_license import fill_license

router = APIRouter(prefix="/license")


@router.get("")
def license_check():
    return {"status": "OK"}


@router.post("/create")
def create_license(student: Student) -> Response:
    content: bytes = fill_license(student)
    return Response(content=content, media_type="image/jpeg")