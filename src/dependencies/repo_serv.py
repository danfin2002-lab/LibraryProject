from typing import Annotated

from fastapi import Depends

from src.dependencies.session import SessionDep
from src.repositories.books import BookRepository
from src.services.books import BookService
from src.repositories.authors import AuthorRepository
from src.services.authors import AuthorService
from src.repositories.libraries import LibraryRepository
from src.services.libraries import LibraryService
from src.repositories.visitors import VisitorRepository
from src.services.visitors import VisitorService
from src.repositories.bl import BLRepository
from src.services.bl import BLService
from src.repositories.arrears import ArrearRepository
from src.services.arrears import ArrearService


#Нужно ли их делать асинхронными
#Books
async def get_book_repository(session: SessionDep) -> BookRepository:
    return BookRepository(session)

BookRepositoryDep = Annotated[BookRepository, Depends(get_book_repository)]

async def get_book_service(book_repository: BookRepositoryDep) -> BookService:
    return BookService(book_repository)

BookServiceDep = Annotated[BookService, Depends(get_book_service)]

#Authors
async def get_author_repository(session: SessionDep)->AuthorRepository:
    return AuthorRepository(session)

AuthorRepositoryDep = Annotated[AuthorRepository, Depends(get_author_repository)]

async def get_author_service(author_repository: AuthorRepositoryDep)->AuthorService:
    return AuthorService(author_repository)

AuthorServiceDep = Annotated[AuthorService, Depends(get_author_service)]

#Libraries
async def get_library_repository(session: SessionDep)->LibraryRepository:
    return  LibraryRepository(session)

LibraryRepositoryDep = Annotated[LibraryRepository, Depends(get_library_repository)]

async def get_library_service(library_repository: LibraryRepositoryDep)->LibraryService:
    return LibraryService(library_repository)

LibraryServiceDep = Annotated[LibraryService, Depends(get_library_service)]

#Visitors
async def get_visitor_repository(session: SessionDep)->VisitorRepository:
    return VisitorRepository(session)

VisitorRepositoryDep = Annotated[VisitorRepository, Depends(get_visitor_repository)]

async def get_visitor_service(visitor_repository: VisitorRepositoryDep)->VisitorService:
    return VisitorService(visitor_repository)

VisitorServiceDep = Annotated[VisitorService, Depends(get_visitor_service)]

#LB
async def get_bl_repository(session: SessionDep)->BLRepository:
	return BLRepository(session)
	
BLRepositoryDep = Annotated[BLRepository, Depends(get_bl_repository)]

async def get_bl_service(bl_repository: BLRepositoryDep)->BLService:
	return BLService(bl_repository)
	
BLServiceDep = Annotated[BLService, Depends(get_bl_service)]


#Arrears
async def get_arrear_repository(session: SessionDep)->ArrearRepository:
	return ArrearRepository(session)
	
ArrearRepositoryDep = Annotated[ArrearRepository, Depends(get_arrear_repository)]

async def get_arrear_service(arrear_repository: ArrearRepositoryDep, visitor_service: VisitorServiceDep, bl_service: BLServiceDep)->ArrearService:
	return ArrearService(arrear_repository, visitor_service, bl_service)
	
ArrearServiceDep = Annotated[ArrearService, Depends(get_arrear_service)]
