from src.dependencies.session import SessionDep
from src.schemas import BLAddSchema, BLSelectSchema
from sqlalchemy import select
from src.models import BL

class BLRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    async def check_BL(self, data: BLAddSchema)->BL:
        existing_bl = await self.session.scalar(
            select(BL).where(BL.book_id == data.book_id,
            BL.library_id == data.library_id
                )
            )
        return existing_bl

    async def add_BL(self, data: BLAddSchema)->BL:
        new_bl = BL(
            book_id = data.book_id,
            library_id = data.library_id,
            count = data.count
        )
        self.session.add(new_bl)
        await self.session.commit()
        return new_bl

    async def get_BL(self, id: int)->BL:
        bl_obj = await self.session.get(BL, id)
        return bl_obj

    async def get_BLs(self)->list[BL]:
        bl_list = (await self.session.scalars(select(BL))).all()
        return bl_list

    async def delete_BL(self, bl_obj: BL):
        await self.session.delete(bl_obj)
        await self.session.commit()

    async def update_BL(self, new_count: int, bl_obj: BL)->BL:
        bl_obj.count = new_count
        await self.session.commit()
        return bl_obj


    