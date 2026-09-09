from sqlalchemy.orm import Session

from models import Cliente as ClienteModel
from models import Projeto as ProjetoModel
from schemas import ProjetoCreate, ProjetoUpdate


def criar_projeto(
    db: Session,
    projeto: ProjetoCreate
):
    cliente = db.query(ClienteModel).filter(
        ClienteModel.id == projeto.cliente_id
    ).first()

    if cliente is None:
        return "CLIENTE_NAO_ENCONTRADO"

    novo_projeto = ProjetoModel(
        cliente_id=projeto.cliente_id,
        nome=projeto.nome,
        descricao=projeto.descricao
    )

    db.add(novo_projeto)
    db.commit()
    db.refresh(novo_projeto)

    return novo_projeto


def listar_projetos(
    db: Session,
    cliente_id: int | None = None,
    page: int = 1,
    limit: int = 10
):
    query = db.query(ProjetoModel)

    if cliente_id is not None:
        query = query.filter(
            ProjetoModel.cliente_id == cliente_id
        )

    total = query.count()

    offset = (page - 1) * limit

    projetos = query.offset(offset).limit(limit).all()

    pages = (total + limit - 1) // limit

    return {
        "projetos": projetos,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages
    }

def buscar_projeto(
    db: Session,
    projeto_id: int
):
    return db.query(ProjetoModel).filter(
        ProjetoModel.id == projeto_id
    ).first()

def atualizar_projeto(
    db: Session,
    projeto_id: int,
    projeto: ProjetoUpdate
):
    projeto_db = db.query(ProjetoModel).filter(
        ProjetoModel.id == projeto_id
    ).first()

    if projeto_db is None:
        return None

    projeto_db.nome = projeto.nome
    projeto_db.descricao = projeto.descricao

    db.commit()
    db.refresh(projeto_db)

    return projeto_db

def excluir_projeto(
    db: Session,
    projeto_id: int
):
    projeto_db = db.query(ProjetoModel).filter(
        ProjetoModel.id == projeto_id
    ).first()

    if projeto_db is None:
        return None

    db.delete(projeto_db)
    db.commit()

    return projeto_db