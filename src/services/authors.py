from src.repositories.authors import AuthorRepository
from src.schemas import AuthorAddSchema
from fastapi import HTTPException
from src.exceptions import AuthorExistsException, AuthorNotFoundException
from src.models import Author

class AuthorService:
    def __init__(self, repository: AuthorRepository):
        self.repository = repository

    async def add_author(self, data: AuthorAddSchema)->Author:
        await self.check_author(data)
        author_obj = await self.repository.add_author(data)
        return author_obj

    async def get_authors(self) -> list[Author]:
        author_list = await self.repository.get_authors()
        return author_list

    async def get_author(self, id: int) -> Author:
        author_obj = await self.repository.get_author(id)
        if author_obj is None:
            raise AuthorNotFoundException("Такой автор не найден")
        return author_obj

    async def check_author(self, data: AuthorAddSchema):
        existing_author = await self.repository.check_author(data)
        if existing_author is not None:
            raise AuthorExistsException("Такой автор уже существует")

    async def update_author(self, id: int, data: AuthorAddSchema ) -> Author:
        author_obj = await self.get_author(id)
        updt_author = await self.repository.update_author(data, author_obj)
        return updt_author

    async def delete_author(self, id: int):
        author_obj = await self.get_author(id)
        await self.repository.delete_author(author_obj)


