from src.dependencies.visitors import VisitorServiceDep
from fastapi import APIRouter, HTTPException, Response, Depends
from src.schemas import VisitorAddSchema, VisitorSelectSchema
from src.exceptions import VisitorExistsException, VisitorNotFoundException
from src.dependencies.active_user import current_active_user
from fastapi.security import HTTPBearer

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix="/visitors", tags=["Посетители"], dependencies=[Depends(current_active_user), Depends(http_bearer)])

@router.post(
	"",
    responses={400:{"descriptions":"Такой посетитель уже существует"},
			 500:{"descriptions":"Не удалось добавить посетителя"}},
    summary="Добавить посетителя",
	response_model=VisitorSelectSchema
)
async def add_visitor(data: VisitorAddSchema, visitor_service: VisitorServiceDep)->VisitorSelectSchema:
	try:
		visitor_obj = await visitor_service.add_visitor(data)
		return visitor_obj
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
	status_code=204,
	responses={404:{"descriptions":"Такой посетитель не найден"},
			   500:{"descriptions":"Не удалось удалить посетителя"}},
	summary="Удалить посетителя")
async def delete(id: int, visitor_service: VisitorServiceDep):
	try:
		await visitor_service.delete_visitor(id)
		return Response(status_code=204)
	except VisitorNotFoundException:
		raise HTTPException(status_code=404, detail="Такой посетитель не найден")
	except Exception:
		raise HTTPException(status_code=500, detail="Не удалось удалить посетителя")

