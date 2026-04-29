from src.schemas import BookAddSchema, BookUpdateSchema
from src.models import Book
from src.dependencies.session import SessionDep
from sqlalchemy import select

class BookRepository:
    def __init__(self, session: SessionDep)->None:
        self.session = session

    async def add_book(self, data: BookAddSchema) -> Book:
        book_obj = Book(
            title=data.title,
            genre=data.genre,
            author_id=data.author_id
        )
        self.session.add(book_obj)
        await self.session.commit()
        return book_obj

    async def get_books(self) -> list[Book]:
        book_list = (await self.session.scalars(select(Book))).all()
        return book_list

    async def get_book(self, id: int) -> Book:
        book_obj = await self.session.get(Book, id)
        return book_obj

    async def check_book(self, data: BookAddSchema)->Book:
        existing_book = await self.session.scalar(
            select(Book).where(Book.title == data.title, Book.genre == data.genre, Book.author_id == data.author_id))
        return existing_book

    async def update_book(self, data: BookUpdateSchema, book_obj: Book)->Book:
        #if data.title is not None:
        #    book_obj.title = data.title
        #if data.genre is not None:
        #    book_obj.genre = data.genre
        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(book_obj, key, value)

        await self.session.commit()
        return book_obj

    async def delete_book(self, book_obj: Book):
        await self.session.delete(book_obj)
        await self.session.commit()




