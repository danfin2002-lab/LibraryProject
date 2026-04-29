from typing import Annotated
from fastapi import Depends
from src.dependencies.session import SessionDep
from src.repositories.books import BookRepository
from src.services.books import BookService
#Books
async def get_book_repository(session: SessionDep) -> BookRepository:
    return BookRepository(session)

BookRepositoryDep = Annotated[BookRepository, Depends(get_book_repository)]

async def get_book_service(book_repository: BookRepositoryDep) -> BookService:
    return BookService(book_repository)

BookServiceDep = Annotated[BookService, Depends(get_book_service)]
