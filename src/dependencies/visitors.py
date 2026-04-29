from typing import Annotated
from fastapi import Depends
from src.dependencies.session import SessionDep
from src.repositories.visitors import VisitorRepository
from src.services.visitors import VisitorService
#Visitors
async def get_visitor_repository(session: SessionDep)->VisitorRepository:
    return VisitorRepository(session)

VisitorRepositoryDep = Annotated[VisitorRepository, Depends(get_visitor_repository)]

async def get_visitor_service(visitor_repository: VisitorRepositoryDep)->VisitorService:
    return VisitorService(visitor_repository)

VisitorServiceDep = Annotated[VisitorService, Depends(get_visitor_service)]