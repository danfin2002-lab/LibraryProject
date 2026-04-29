from src.schemas import ArrearAddSchema, ArrearSelectSchema
from sqlalchemy import select
from src.dependencies.session import SessionDep
from src.models import Arrear

class ArrearRepository:
	def __init__(self, session: SessionDep):
		self.session = session
	
	#add
	async def add_arrear(self, data: ArrearAddSchema)->Arrear:
		new_arrear = Arrear(
			book_id = data.book_id,
			library_id = data.library_id,
			visitor_id = data.visitor_id
		)
		self.session.add(new_arrear)
		await self.session.commit()
		return new_arrear
	#get
	async def get_arrear(self, id: int)->Arrear:
		arrear_obj = await self.session.get(Arrear, id)
		return arrear_obj
	#get
	async def get_arrears(self)->list[Arrear]:
		arrears_list = (await self.session.scalars(select(Arrear))).all()
		return arrears_list
	#delete
	async def delete_arrear(self, arrear_obj: Arrear):
		await self.session.delete(arrear_obj)
		await self.session.commit()
		