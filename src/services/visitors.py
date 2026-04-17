from src.repositories.visitors import VisitorRepository
from src.schemas import VisitorAddSchema, VisitorSelectSchema
from fastapi import HTTPException
from src.exceptions import VisitorExistsException, VisitorNotFoundException

class VisitorService:
	def __init__(self, repository: VisitorRepository):
		self.repository = repository
	
	async def add_visitor(self, data: VisitorAddSchema):
		await self.check_visitor(data)
		await self.repository.add_visitor(data)
		return {"ok": "Посетитель успешно добавлен"}
	
	async def check_visitor(self, data: VisitorAddSchema):
		visitor_obj = await self.repository.check_visitor(data)
		if visitor_obj is not None:
			raise VisitorExistsException("Такой посетитель уже существует")
	
	async def get_visitor(self, id: int)->VisitorSelectSchema:
		visitor_obj = await self.repository.get_visitor(id)
		if visitor_obj is None:
			raise VisitorNotFoundException("Такой посетитель не найден")
		return visitor_obj
	
	async def get_visitors(self)->list[VisitorSelectSchema]:
		visitor_list = await self.repository.get_visitors()
		return visitor_list
		
	async def update_visitor(self, data: VisitorAddSchema, id: int)->VisitorSelectSchema:
		visitor_obj = await self.get_visitor(id)
		updt_visitor = await self.repository.update_visitor(data, visitor_obj)
		return updt_visitor
			
	async def delete_visitor(self, id: int):
		visitor_obj = await self.get_visitor(id)
		await self.repository.delete_visitor(visitor_obj)
		return {"ok": "Посетитель успешно удалён"}
		
		