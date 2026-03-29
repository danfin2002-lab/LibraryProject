from os import name

from sqlalchemy import select

from database import async_engine,sync_engine, sync_session_factory, async_session_factory
from models import Author, Book, Base

# def create_tables():
#     sync_engine.echo = True
#     Base.metadata.drop_all(sync_engine)
#     Base.metadata.create_all(sync_engine)
# def insert_author():
#     author_london = Author(name = "Jack London")
#     with sync_session_factory() as session:
#         session.add(author_london)
#         session.commit()
#
# def insert_book():
#     with sync_session_factory() as session:
#         author = session.execute(select(Author).where(Author.name == "Jack London"))
#         book_iden = Book(title="Martin Iden", genre="Novel", author_id=author.first().id)
#         session.add(book_iden)
#         session.commit()



async def create_tables():
    async with async_engine.begin() as conn:
        async_engine.echo = True
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
async def delete_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
async def insert_author():
    author_london = Author(name = "Jack London")
    async with async_session_factory() as session:
        session.add(author_london)
        await session.commit()

async def insert_book():
    async with async_session_factory() as session:
        author = await session.scalar(select(Author).where(Author.name == "Jack London"))
        book_iden = Book(title="Martin Iden", genre="Novel", author_id=author.id)
        session.add(book_iden)
        await session.commit()