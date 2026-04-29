from src.repositories.bl import BLRepository
from src.schemas import BLAddSchema
from fastapi import HTTPException
from src.models import BL
from src.exceptions import BLNotFoundException

class BLService:
    def __init__(self, repository: BLRepository):
        self.max_count = 1000
        self.repository = repository

    async def get_BL_by_id(self, book_id: int, library_id: int)->BL:
        data = BLAddSchema(book_id=book_id, library_id=library_id, count=self.max_count)
        existing_bl = await self.check_BL(data)
        if existing_bl is None:
            raise BLNotFoundException("Такой книги в библиотеке нет")
        return existing_bl

    async def check_BL(self, data: BLAddSchema)->BL:
        existing_bl = await self.repository.check_BL(data) # Возвращает BL
        return existing_bl
		
    async def add_BL(self, data: BLAddSchema)->BL:
        existing_bl = await self.check_BL(data)
        if existing_bl is None:
            bl_obj = await self.repository.add_BL(data)
            return bl_obj
        else:
            updt_obj = await self.update_BL(data.count, existing_bl)
            return updt_obj

    async def get_BL(self, id: int)->BL:
        bl_obj = await self.repository.get_BL(id)
        if bl_obj is None:
            raise BLNotFoundException("Такой связи книга-библиотека нет")
        return bl_obj

    async def get_BLs(self)->list[BL]:
        bl_list = await self.repository.get_BLs()
        return bl_list

    async def delete_BL(self, id: int):
        bl_obj = await self.get_BL(id)
        await self.repository.delete_BL(bl_obj)

    async def update_BL(self, add_count: int, bl_obj: BL)->BL:
        new_count = bl_obj.count + add_count
        if new_count <= self.max_count:
            updt_obj = await self.repository.update_BL(new_count, bl_obj)
        else:
            updt_obj = await self.repository.update_BL(self.max_count, bl_obj)
        return updt_obj



