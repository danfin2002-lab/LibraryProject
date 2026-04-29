from typing import Annotated
from fastapi import Depends
from src.dependencies.session import SessionDep
from src.repositories.authors import AuthorRepository
from src.services.authors import AuthorService
#Authors
async def get_author_repository(session: SessionDep)->AuthorRepository:
    return AuthorRepository(session)

AuthorRepositoryDep = Annotated[AuthorRepository, Depends(get_author_repository)]

async def get_author_service(author_repository: AuthorRepositoryDep)->AuthorService:
    return AuthorService(author_repository)

AuthorServiceDep = Annotated[AuthorService, Depends(get_author_service)]