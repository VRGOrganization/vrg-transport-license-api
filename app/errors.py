from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorSpec:
    code: str
    status: int
    message: str


ERROR_CATALOG: dict[str, ErrorSpec] = {
    "ERR001": ErrorSpec(code="ERR001", status=403, message="Nao autorizado"),
    "ERR002": ErrorSpec(code="ERR002", status=400, message="Formato de foto invalido (base64)"),
    "ERR003": ErrorSpec(code="ERR003", status=400, message="Formato de imagem nao suportado"),
    "ERR004": ErrorSpec(code="ERR004", status=400, message="Erro ao processar foto"),
    "ERR010": ErrorSpec(code="ERR010", status=500, message="Template da carteirinha nao encontrado"),
    "ERR011": ErrorSpec(code="ERR011", status=500, message="Template da carteirinha invalido"),
    "ERR012": ErrorSpec(code="ERR012", status=500, message="Erro ao carregar template"),
    "ERR099": ErrorSpec(code="ERR099", status=500, message="Erro interno inesperado"),
}


class AppError(Exception):
    def __init__(self, code: str, *, origin: str, context: dict | None = None):
        spec = ERROR_CATALOG.get(code)
        if spec is None:
            raise ValueError(f"Error code not found in catalog: {code}")

        self.code = spec.code
        self.status = spec.status
        self.origin = origin
        self.context = context or {}
        self.public_payload = {"code": self.code, "status": self.status}
        super().__init__(spec.message)
