from fastapi import FastAPI

from routers.clientes import router as clientes_router


app = FastAPI()


app.include_router(clientes_router)


@app.get("/")
def home():
    return {"mensagem": "API funcionando!"}