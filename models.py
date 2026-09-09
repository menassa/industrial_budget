from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    telefone: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    projetos: Mapped[list["Projeto"]] = relationship(
        back_populates="cliente"
    )


class Projeto(Base):
    __tablename__ = "projetos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id"),
        nullable=False
    )

    nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    descricao: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default="ATIVO"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    cliente: Mapped["Cliente"] = relationship(
        back_populates="projetos"
    )