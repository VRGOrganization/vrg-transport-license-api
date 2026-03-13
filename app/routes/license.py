import base64

from fastapi import APIRouter, Header, Request
from fastapi.responses import JSONResponse

from app.config import API_KEY
from app.errors import AppError
from app.schemas.student import Student
from app.operations_log import operations_logger
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
    request: Request,
    x_api_key: str | None = Header(default=None),
):
    if API_KEY is not None and x_api_key != API_KEY:
        raise AppError(
            code="ERR001",
            origin="route.license.auth",
            context={"employee_id": student.employee_id},
        )

    image_bytes: bytes = fill_license(student)
    image_base64: str = base64.b64encode(image_bytes).decode("utf-8")

    operations_logger.log(
        {
            "operacao": "criar_carteirinha",
            "status": "sucesso",
            "status_http": 201,
            "id_requisicao": getattr(request.state, "request_id", None),
            "caminho": str(request.url.path),
            "contexto": {
                "id_estudante": student.id,
                "id_funcionario": student.employee_id,
            },
        }
    )

    return JSONResponse(
        status_code=201,
        content={"image": image_base64},
    )