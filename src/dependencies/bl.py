from typing import Annotated
from fastapi import Depends
from src.dependencies.session import SessionDep
from src.repositories.bl import BLRepository
from src.services.bl import BLService
#BL
async def get_bl_repository(session: SessionDep)->BLRepository:
	return BLRepository(session)
	
BLRepositoryDep = Annotated[BLRepository, Depends(get_bl_repository)]

async def get_bl_service(bl_repository: BLRepositoryDep)->BLService:
	return BLService(bl_repository)
	
BLServiceDep = Annotated[BLService, Depends(get_bl_service)]