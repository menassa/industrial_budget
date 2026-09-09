from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from routers.clientes import router as clientes_router
from routers.projetos import router as projetos_router

app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    if isinstance(exc.detail, dict):
        content = exc.detail
    else:
        content = {
            "error": "HTTP_ERROR",
            "message": str(exc.detail)
        }

    return JSONResponse(
        status_code=exc.status_code,
        content=content
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    fields = []

    for error in exc.errors():
        location = error.get("loc", [])
        field = location[-1] if location else "desconhecido"
        error_type = error.get("type")

        messages = {
            "greater_than_equal": "O valor deve ser maior ou igual a 1.",
            "less_than_equal": "O valor deve ser menor ou igual a 100.",
            "string_too_short": "O texto informado é muito curto.",
            "string_too_long": "O texto informado é muito longo.",
            "value_error": "O valor informado é inválido.",
            "value_error.email": "Informe um endereço de e-mail válido.",
        }

        message = messages.get(
            error_type,
            error.get("msg", "Valor inválido.")
        )

        fields.append({
            "field": str(field),
            "message": message
    })

    return JSONResponse(
        status_code=422,
        content={
            "error": "DADOS_INVALIDOS",
            "message": "Existem campos inválidos na requisição.",
            "fields": fields
        }
    )


app.include_router(clientes_router)
app.include_router(projetos_router)

@app.get("/")
def home():
    return {"mensagem": "API funcionando!"}