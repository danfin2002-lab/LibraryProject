import datetime
import uuid
from sqlalchemy import String, ForeignKey, CheckConstraint, UUID
from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase


intpk = Annotated[int, mapped_column(primary_key=True)]
strname = Annotated[str, mapped_column(String(30))]


class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[intpk]
    name: Mapped[strname] = mapped_column(unique=True)

class Book(Base):
    __tablename__ = "books"

    id: Mapped[intpk]
    title: Mapped[str]
    genre: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE") )

class Library(Base):
    __tablename__ = "libraries"

    id: Mapped[intpk]
    address: Mapped[str] = mapped_column(unique=True)

class Visitor(Base):
    __tablename__ = "visitors"

    id: Mapped[intpk]
    name: Mapped[strname]
    birthday: Mapped[datetime.date]


class Arrear(Base):
    __tablename__ = "arrears"

    id: Mapped[intpk]
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))
    visitor_id: Mapped[int] = mapped_column(ForeignKey("visitors.id", ondelete="CASCADE"))
    library_id: Mapped[int] = mapped_column(ForeignKey("libraries.id", ondelete="CASCADE"))

class BL(Base):
    __tablename__ = "book_libraries"
    __table_args__ = (
        CheckConstraint('count <= 1000', name='check_count_max'),
    )

    id: Mapped[intpk]
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))
    library_id: Mapped[int] = mapped_column(ForeignKey("libraries.id", ondelete="CASCADE"))
    count: Mapped[int]

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )