import logging
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.errors import AppError
from app.operations_log import operations_logger
from app.routes import health, license

app = FastAPI()


"""
intercepta todas as requisições, gera um request_id único, 
guarda em request.state e adiciona no header X-Request-Id da resposta para rastreamento.
"""
@app.middleware("http")
async def add_request_id(request: Request, call_next):
	request_id = str(uuid.uuid4())
	request.state.request_id = request_id
	response = await call_next(request)
	response.headers["X-Request-Id"] = request_id
	return response


# Captura erros previstos da aplicação, registra no log de operações com contexto e devolve apenas code e status.
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
	operations_logger.log(
		{
			"operacao": "criar_carteirinha",
			"status": "erro",
			"status_http": exc.status,
			"codigo_erro": exc.code,
			"origem": exc.origin,
			"id_requisicao": getattr(request.state, "request_id", None),
			"caminho": str(request.url.path),
			"contexto": exc.context,
		}
	)
	return JSONResponse(status_code=exc.status, content=exc.public_payload)

# Captura qualquer erro não previsto, escreve stacktrace no console e registra um erro genérico (ERR099) no log de operações.
@app.exception_handler(Exception)
async def unexpected_error_handler(request: Request, exc: Exception):
	logging.exception("erro_inesperado id_requisicao=%s", getattr(request.state, "request_id", None))
	operations_logger.log(
		{
			"operacao": "criar_carteirinha",
			"status": "erro",
			"status_http": 500,
			"codigo_erro": "ERR099",
			"origem": "global.inesperado",
			"id_requisicao": getattr(request.state, "request_id", None),
			"caminho": str(request.url.path),
			"contexto": {"erro": str(exc)},
		}
	)
	return JSONResponse(status_code=500, content={"code": "ERR099", "status": 500})

app.include_router(health.router)
app.include_router(license.router)