from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db

from schemas import (
    ProjetoCreate,
    ProjetoListResponse,
    ProjetoResponse,
    ProjetoUpdate
)

from services.projetos import (
    criar_projeto,
    listar_projetos,
    buscar_projeto,
    atualizar_projeto,
    excluir_projeto
)


router = APIRouter(
    prefix="/projetos",
    tags=["Projetos"]
)


@router.post("/", response_model=ProjetoResponse, status_code=201)
def criar_novo_projeto(
    projeto: ProjetoCreate,
    db: Session = Depends(get_db)
):
    novo_projeto = criar_projeto(
    db,
    projeto
)

    if novo_projeto == "CLIENTE_NAO_ENCONTRADO":
      raise HTTPException(
        status_code=404,
        detail={
          "error": "CLIENTE_NAO_ENCONTRADO",
          "message": "O cliente informado não existe."
        }
      )

    return novo_projeto

@router.get("/", response_model=ProjetoListResponse)
def listar_projetos_endpoint(
    cliente_id: int | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    projetos = listar_projetos(
        db,
        cliente_id,
        page,
        limit
    )

    return projetos

@router.get("/{projeto_id}", response_model=ProjetoResponse)
def buscar_projeto_endpoint(
    projeto_id: int,
    db: Session = Depends(get_db)
):
    projeto = buscar_projeto(
        db,
        projeto_id
    )

    if projeto is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "PROJETO_NAO_ENCONTRADO",
                "message": "Projeto não encontrado."
            }
        )

    return projeto

@router.put("/{projeto_id}", response_model=ProjetoResponse)
def atualizar_projeto_endpoint(
    projeto_id: int,
    projeto: ProjetoUpdate,
    db: Session = Depends(get_db)
):
    projeto_atualizado = atualizar_projeto(
        db,
        projeto_id,
        projeto
    )

    if projeto_atualizado is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "PROJETO_NAO_ENCONTRADO",
                "message": "Projeto não encontrado."
            }
        )

    return projeto_atualizado

@router.delete("/{projeto_id}", response_model=ProjetoResponse)
def excluir_projeto_endpoint(
    projeto_id: int,
    db: Session = Depends(get_db)
):
    projeto_excluido = excluir_projeto(
        db,
        projeto_id
    )

    if projeto_excluido is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "PROJETO_NAO_ENCONTRADO",
                "message": "Projeto não encontrado."
            }
        )

    return projeto_excluido