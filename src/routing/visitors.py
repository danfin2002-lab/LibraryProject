from src.dependencies.repo_serv import VisitorServiceDep
from fastapi import APIRouter, HTTPException
from src.schemas import VisitorAddSchema, VisitorSelectSchema
from src.exceptions import VisitorExistsException, VisitorNotFoundException

router = APIRouter(prefix="/visitors", tags=["Посетители"])

@router.post("",
    responses={400:{"descriptions":"Такой посетитель уже существует"},
			 500:{"descriptions":"Не удалось добавить посетителя"}},
    summary="Добавить посетителя")
async def add_visitor(data: VisitorAddSchema, visitor_service: VisitorServiceDep):
	try:
		return await visitor_service.add_visitor(data)
	except VisitorExistsException:
		raise HTTPException(status_code=400, detail="Такой посетитель уже существует")
	except Exception:
		raise HTTPException(status_code=500, detail="Не удалось добавить посетителя")
		
@router.get("",
    responses={500:{"descriptions":"Не удалось получить посетителей"}},
	summary="Получить всех посетителей",
	response_model=list[VisitorSelectSchema])
async def get_visitors(visitor_service: VisitorServiceDep)->list[VisitorSelectSchema]:
	try:	
		visitor_list = await visitor_service.get_visitors()
		return visitor_list
	except Exception:
		raise HTTPException(status_code=500, detail="Не удалось получить посетителей")
		
@router.get("/{id}",
	responses={404:{"descriptions":"Такой посетитель не найден"}},
	summary="Получить посетителя по id",
	response_model=VisitorSelectSchema)
async def get_visitor(id: int, visitor_service: VisitorServiceDep)->VisitorSelectSchema:
	try:
		visitor_obj = await visitor_service.get_visitor(id)
		return visitor_obj
	except VisitorNotFoundException:
		raise HTTPException(status_code=404, detail="Такой посетитель не найден")
		
@router.patch("/{id}",
	responses={404:{"descriptions":"Такой посетитель не найден"},
			   500:{"descriptions":"Не удалось обновить посетителя"}},
	summary="Обновить информацию о посетителе",
	response_model=VisitorSelectSchema)
async def update_visitor(id: int, data: VisitorAddSchema, visitor_service: VisitorServiceDep)->VisitorSelectSchema:
	try:
		updt_visitor = await visitor_service.update_visitor(data, id)
		return updt_visitor
	except VisitorNotFoundException:
		raise HTTPException(status_code=404, detail="Такой посетитель не найден")
	except Exception:
		raise HTTPException(status_code=500, detail="Не удалось обновить посетителя")
		
@router.delete("/id",
	responses={404:{"descriptions":"Такой посетитель не найден"},
			   500:{"descriptions":"Не удалось удалить посетителя"}},
	summary="Удалить посетителя")
async def delete(id: int, visitor_service: VisitorServiceDep):
	try:
		return await visitor_service.delete_visitor(id)
	except VisitorNotFoundException:
		raise HTTPException(status_code=404, detail="Такой посетитель не найден")
	except Exception:
		raise HTTPException(status_code=500, detail="Не удалось удалить посетителя")

