from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClienteCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: EmailStr
    telefone: str = Field(min_length=8, max_length=20)


class ClienteUpdate(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: EmailStr
    telefone: str = Field(min_length=8, max_length=20)


class ClienteResponse(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str

    model_config = ConfigDict(from_attributes=True)


class ClienteListResponse(BaseModel):
    clientes: list[ClienteResponse]
    page: int
    limit: int
    total: int
    pages: int

class ProjetoCreate(BaseModel):
    cliente_id: int
    nome: str = Field(min_length=2, max_length=150)
    descricao: str | None = Field(default=None, max_length=500)


class ProjetoUpdate(BaseModel):
    nome: str = Field(min_length=2, max_length=150)
    descricao: str | None = Field(default=None, max_length=500)


class ProjetoResponse(BaseModel):
    id: int
    cliente_id: int
    nome: str
    descricao: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProjetoListResponse(BaseModel):
    projetos: list[ProjetoResponse]
    page: int
    limit: int
    total: int
    pages: int

class ErrorField(BaseModel):
    field: str
    message: str


class ErrorResponse(BaseModel):
    error: str
    message: str
    fields: list[ErrorField] | None = None