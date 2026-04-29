from src.dependencies.session import SessionDep
from src.schemas import VisitorAddSchema, VisitorSelectSchema
from src.models import Visitor
from sqlalchemy import select

class VisitorRepository:
	def __init__(self, session: SessionDep):
		self.session = session
	
	#add_visitor
	async def add_visitor(self, data: VisitorAddSchema)-> Visitor:
		visitor_obj = Visitor(
			name = data.name,
			birthday = data.birthday
		)
		self.session.add(visitor_obj)
		await self.session.commit()
		return visitor_obj
#check_visitor
	async def check_visitor(self, data: VisitorAddSchema)->Visitor:
		existing_visitor = await self.session.scalar(
		select(Visitor).where(
			Visitor.name == data.name, Visitor.birthday == data.birthday
			)
		)
		return existing_visitor

#get_visitors
	async def get_visitors(self)->list[Visitor]:
		visitor_list = (await self.session.scalars(select(Visitor))).all()
		return visitor_list
#get_visitor(по id)
	async def get_visitor(self, id: int)->Visitor:
		visitor_obj = await self.session.get(Visitor, id)
		return visitor_obj
#update_visitor
	async def update_visitor(self, data: VisitorAddSchema, visitor_obj: Visitor)->Visitor:
		#if data.name is not None:
		#	visitor_obj.name = data.name
		#if data.birthday is not None:
		#	visitor_obj.birthday = data.birthday
		update_data = data.model_dump(exclude_unset=True)
		
		for key, value in update_data.items():
			setattr(visitor_obj, key, value)
		
		
		await self.session.commit()
		return visitor_obj
#delete_visitor
	async def delete_visitor(self, visitor_obj: Visitor):
		await self.session.delete(visitor_obj)
		await self.session.commit()

