from src.repositories.arrears import ArrearRepository
from src.schemas import ArrearAddSchema, ArrearSelectSchema
from src.services.visitors import VisitorService
from src.services.bl import BLService
from src.exceptions import ArrearNotFoundException, BookNotEnoughException
from src.models import Arrear

class ArrearService:
    def __init__(self, repository: ArrearRepository, visitor_service: VisitorService, bl_service: BLService):
        self.repository = repository
        self.visitor_service = visitor_service
        self.bl_service = bl_service

    async def add_arrear(self, data: ArrearAddSchema)->Arrear:
        await self.visitor_service.get_visitor(data.visitor_id) 
        existing_bl = await self.bl_service.get_BL_by_id(data.book_id, data.library_id)
        if existing_bl.count > 0:
            arrear_obj = await self.repository.add_arrear(data)
            await self.bl_service.update_BL(-1, existing_bl)
            return arrear_obj
        else:
            raise BookNotEnoughException("Таких книг недостаточно в библиотеке")
            

    async def get_arrears(self)->list[Arrear]:
        arrears_list = await self.repository.get_arrears()
        return arrears_list

    async def get_arrear(self, id: int)->Arrear:
        arrear_obj = await self.repository.get_arrear(id)
        if arrear_obj is None:
            raise ArrearNotFoundException("Такая задолженность не найдена")
        return arrear_obj

    async def delete_arrear(self, id: int):
        arrear_obj = await self.get_arrear(id)
        bl_obj = await self.bl_service.get_BL_by_id(arrear_obj.book_id, arrear_obj.library_id)
        await self.repository.delete_arrear(arrear_obj)
        await self.bl_service.update_BL(1, bl_obj)


