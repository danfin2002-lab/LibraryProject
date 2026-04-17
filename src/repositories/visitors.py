from src.dependencies.session import SessionDep
from src.schemas import VisitorAddSchema, VisitorSelectSchema
from src.models import Visitor
from sqlalchemy import select

class VisitorRepository:
	def __init__(self, session: SessionDep):
		self.session = session
	
	#add_visitor
	async def add_visitor(self, data: VisitorAddSchema):
		visitor_obj = Visitor(
			name = data.name,
			birthday = data.birthday
		)
		self.session.add(visitor_obj)
		await self.session.commit()
#check_visitor
	async def check_visitor(self, data: VisitorAddSchema)->VisitorSelectSchema:
		existing_visitor = await self.session.scalar(
		select(Visitor).where(
			Visitor.name == data.name, Visitor.birthday == data.birthday
			)
		)
		return existing_visitor

#get_visitors
	async def get_visitors(self)->list[VisitorSelectSchema]:
		visitor_list = (await self.session.scalars(select(Visitor))).all()
		return visitor_list
#get_visitor(по id)
	async def get_visitor(self, id: int)->VisitorSelectSchema:
		visitor_obj = await self.session.get(Visitor, id)
		return visitor_obj
#update_visitor
	async def update_visitor(self, data: VisitorAddSchema, visitor_obj: VisitorSelectSchema)->VisitorSelectSchema:
		if data.name is not None:
			visitor_obj.name = data.name
		if data.birthday is not None:
			visitor_obj.birthday = data.birthday
		
		await self.session.commit()
		return visitor_obj
#delete_visitor
	async def delete_visitor(self, visitor_obj: VisitorSelectSchema):
		await self.session.delete(visitor_obj)
		await self.session.commit()

