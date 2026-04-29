from src.repositories.books import BookRepository
from src.schemas import BookAddSchema, BookUpdateSchema
from fastapi import HTTPException
from src.exceptions import BookExistsException, BookNotFoundException
from src.models import Book

class BookService:
    def __init__(self, repository: BookRepository)->None:
        self.repository = repository

    async def add_book(self, data: BookAddSchema)->Book:
        await self.check_book(data)
        book_obj = await self.repository.add_book(data)
        return book_obj
		
    async def get_books(self)->list[Book]:
        book_list = await self.repository.get_books()
        return book_list

    async def get_book(self, id: int) -> Book:
        book_obj = await self.repository.get_book(id)
        if book_obj is None:
            raise BookNotFoundException("Такая книга не найдена")
        return book_obj

    async def check_book(self, data: BookAddSchema):
        existing_book = await self.repository.check_book(data)
        if existing_book is not None:
            raise BookExistsException("Такая книга уже существует")

    async def update_book(self, id: int, data: BookUpdateSchema)->Book:
        book_obj = await self.get_book(id)
        updt_book = await self.repository.update_book(data, book_obj)
        return updt_book

    async def delete_book(self, id: int):
        book_obj = await self.get_book(id)
        await self.repository.delete_book(book_obj)

