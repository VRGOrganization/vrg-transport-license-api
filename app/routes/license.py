import base64

from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse

from app.config import API_KEY
from app.schemas.student import Student
from app.services.fill_license import fill_license

router = APIRouter(prefix="/api/v1/license")

"""
Gera a carteirinha do estudante e retorna a imagem em base64.

Valida a chave de autorizacao via header X-Api-Key.
Retorna 201 com a imagem, 403 se nao autorizado, ou 422 se faltar campos.

"""
@router.post("/create", status_code=201)
def create_license(
    student: Student,
    x_api_key: str | None = Header(default=None),
):
    if API_KEY is not None and x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Nao autorizado")

    image_bytes: bytes = fill_license(student)
    image_base64: str = base64.b64encode(image_bytes).decode("utf-8")

    return JSONResponse(
        status_code=201,
        content={"image": image_base64},
    )