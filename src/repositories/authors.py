from typing import Annotated

from src.models import Author
from src.schemas import AuthorAddSchema, AuthorSelectSchema
from src.dependencies.session import SessionDep
from sqlalchemy import select

class AuthorRepository:
    def __init__(self, session: SessionDep):
        self.session = session
#check
    async def check_author(self, data: AuthorAddSchema) -> AuthorSelectSchema:
        existing_author = await self.session.scalar(
            select(Author).where(Author.name == data.name)
        )
        return existing_author
#add
    async def add_author(self, data: AuthorAddSchema):
        new_author = Author(
            name=data.name
        )
        self.session.add(new_author)
        await self.session.commit()
#get_all
    async def get_authors(self) -> list[AuthorSelectSchema]:
        author_list = (await self.session.scalars(select(Author))).all()
        return author_list
#get_by_id
    async def get_author(self, id: int) -> AuthorSelectSchema:
        author_obj = await self.session.get(Author, id)
        return author_obj
#patch
    async def update_author(self, data: AuthorAddSchema, author_obj: AuthorSelectSchema)->AuthorSelectSchema:
        if data.name is not None:
            author_obj.name = data.name
        #Нужно ли добавлять в сессию?
        await self.session.commit()
        return author_obj
#delete
    async def delete_author(self, author_obj: AuthorSelectSchema):
        await self.session.delete(author_obj)
        await self.session.commit()

async def get_author_repository(session: SessionDep)->AuthorRepository:
    return AuthorRepository(session)

AuthorRepositoryDep = Annotated[AuthorRepository, get_author_repository]
