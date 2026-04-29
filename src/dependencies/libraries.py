from typing import Annotated
from fastapi import Depends
from src.dependencies.session import SessionDep
from src.repositories.libraries import LibraryRepository
from src.services.libraries import LibraryService
#Libraries
async def get_library_repository(session: SessionDep)->LibraryRepository:
    return  LibraryRepository(session)

LibraryRepositoryDep = Annotated[LibraryRepository, Depends(get_library_repository)]

async def get_library_service(library_repository: LibraryRepositoryDep)->LibraryService:
    return LibraryService(library_repository)

LibraryServiceDep = Annotated[LibraryService, Depends(get_library_service)]