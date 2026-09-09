from pydantic import BaseModel, ConfigDict


class ClienteCreate(BaseModel):
    nome: str
    email: str
    telefone: str


class ClienteResponse(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str

    model_config = ConfigDict(from_attributes=True)


class ClienteListResponse(BaseModel):
    clientes: list[ClienteResponse]