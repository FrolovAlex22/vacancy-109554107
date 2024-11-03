from enum import Enum as PyEnum

from sqlalchemy import (
    Enum,
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class StatusTaskEnum(PyEnum):
    WAITING = "ожидает"
    IN_PROGRESS = "в процессе"
    DONE = "завершена"
    IN_ARCHIVE = "в архиве"


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(70), nullable=False)


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String, index=True)
    status: Mapped[StatusTaskEnum] = mapped_column(
        Enum(StatusTaskEnum),
        default=StatusTaskEnum.WAITING,
        server_default="WAITING",
        nullable=True,
    )
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
