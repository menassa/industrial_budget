from sqlalchemy.orm import Session

from models import Cliente as ClienteModel
from schemas import ClienteCreate, ClienteUpdate


def criar_cliente(
    db: Session,
    cliente: ClienteCreate
):
    cliente_existente = db.query(ClienteModel).filter(
        ClienteModel.email == cliente.email
    ).first()

    if cliente_existente is not None:
        return "EMAIL_DUPLICADO"

    novo_cliente = ClienteModel(
        nome=cliente.nome,
        email=cliente.email,
        telefone=cliente.telefone
    )

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return novo_cliente


def listar_clientes(
    db: Session,
    nome: str | None = None,
    page: int = 1,
    limit: int = 10
):
    query = db.query(ClienteModel)

    if nome:
        query = query.filter(
            ClienteModel.nome.ilike(f"%{nome}%")
        )

    total = query.count()

    offset = (page - 1) * limit

    clientes = query.offset(offset).limit(limit).all()

    pages = (total + limit - 1) // limit

    return {
        "clientes": clientes,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages
    }


def buscar_cliente(
    db: Session,
    cliente_id: int
):
    return db.query(ClienteModel).filter(
        ClienteModel.id == cliente_id
    ).first()

def atualizar_cliente(
    db: Session,
    cliente_id: int,
    cliente: ClienteUpdate
):
    cliente_db = db.query(ClienteModel).filter(
        ClienteModel.id == cliente_id
    ).first()

    if cliente_db is None:
        return None

    cliente_db.nome = cliente.nome
    cliente_db.email = cliente.email
    cliente_db.telefone = cliente.telefone

    db.commit()
    db.refresh(cliente_db)

    return cliente_db

def excluir_cliente(
    db: Session,
    cliente_id: int
):
    cliente_db = db.query(ClienteModel).filter(
        ClienteModel.id == cliente_id
    ).first()

    if cliente_db is None:
        return None

    db.delete(cliente_db)
    db.commit()

    return cliente_db