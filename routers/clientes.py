from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import ClienteCreate, ClienteResponse, ClienteListResponse

from services.clientes import (
    criar_cliente as criar_cliente_service,
    listar_clientes as listar_clientes_service,
    buscar_cliente as buscar_cliente_service,
    atualizar_cliente as atualizar_cliente_service,
    excluir_cliente as excluir_cliente_service
)

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


@router.post("/", response_model=ClienteResponse)
def criar_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):
    novo_cliente = criar_cliente_service(
        db,
        cliente
    )

    return novo_cliente

@router.get("/", response_model=ClienteListResponse)
def listar_clientes(
    db: Session = Depends(get_db)
):
    clientes = listar_clientes_service(db)

    return {
        "clientes": clientes
    }

@router.get("/{cliente_id}", response_model=ClienteResponse)
def buscar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    cliente = buscar_cliente_service(
        db,
        cliente_id
    )

    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado!"
        )

    return cliente

@router.put("/{cliente_id}", response_model=ClienteResponse)
def atualizar_cliente(
    cliente_id: int,
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):
    cliente_atualizado = atualizar_cliente_service(
        db,
        cliente_id,
        cliente
    )

    if cliente_atualizado is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado!"
        )

    return cliente_atualizado

@router.delete("/{cliente_id}", response_model=ClienteResponse)
def excluir_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    cliente_excluido = excluir_cliente_service(
        db,
        cliente_id
    )

    if cliente_excluido is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado!"
        )

    return cliente_excluido