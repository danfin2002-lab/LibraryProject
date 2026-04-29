from typing import Annotated
from fastapi import Depends
from src.dependencies.session import SessionDep
from src.repositories.arrears import ArrearRepository
from src.services.arrears import ArrearService
from src.dependencies.visitors import VisitorServiceDep
from src.dependencies.bl import BLServiceDep
#Arrears
async def get_arrear_repository(session: SessionDep)->ArrearRepository:
	return ArrearRepository(session)
	
ArrearRepositoryDep = Annotated[ArrearRepository, Depends(get_arrear_repository)]

async def get_arrear_service(arrear_repository: ArrearRepositoryDep, visitor_service: VisitorServiceDep, bl_service: BLServiceDep)->ArrearService:
	return ArrearService(arrear_repository, visitor_service, bl_service)
	
ArrearServiceDep = Annotated[ArrearService, Depends(get_arrear_service)]