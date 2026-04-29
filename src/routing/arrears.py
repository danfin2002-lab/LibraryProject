from src.schemas import ArrearAddSchema, ArrearSelectSchema
from src.dependencies.arrears import ArrearServiceDep
from fastapi import HTTPException, APIRouter, Response, Depends
from src.exceptions import VisitorNotFoundException, BLNotFoundException, ArrearNotFoundException, BookNotEnoughException
from src.dependencies.active_user import current_active_user
from fastapi.security import HTTPBearer

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/arrears", tags=["Задолженности"], dependencies=[Depends(current_active_user), Depends(http_bearer)])

@router.post(
	"",
	responses={404:{"description":"Такого посетителя или такой связи книга-библиотека нет"},
			   409:{"description":"Таких книг недостаточно в библиотеке"},
			   500:{"description":"Не удалось добавить задолженность"}},
	summary="Добавить задолженность",
	response_model=ArrearSelectSchema
)
async def add_arrear(data: ArrearAddSchema, arrear_service: ArrearServiceDep)->ArrearSelectSchema:
	try:
		arrear_obj = await arrear_service.add_arrear(data)
		return arrear_obj
	except VisitorNotFoundException:
		raise HTTPException(status_code=404, detail="Такой посетитель не найден")
	except BLNotFoundException:
		raise HTTPException(status_code=404, detail="Такая связь книга-библиотека не найдена")
	except BookNotEnoughException:
		raise HTTPException(status_code=409, detail="Таких книг недостаточно в библиотеке")
	except Exception:
		raise HTTPException(status_code=500, detail="Не удалось добавить задолженность")
	
@router.get(
	"{/id}",
	responses={404:{"description":"Такая задолженность не найдена"}},
	summary = "Получить задолженность",
	response_model = ArrearSelectSchema
)
async def get_arrear(id: int, arrear_service: ArrearServiceDep)->ArrearSelectSchema:
	try:	
		arrear_obj = await arrear_service.get_arrear(id)
		return arrear_obj
	except ArrearNotFoundException:
		raise HTTPException(status_code=404, detail="Такая задолженность не найдена")
	
@router.get(
	"",
	responses={500:{"description":"Не удалось получить задолженности"}},
	summary="Получить все задолженности",
	response_model=list[ArrearSelectSchema]
)
async def ger_arrears(arrear_service: ArrearServiceDep)->list[ArrearSelectSchema]:
	try:
		arrears_list = await arrear_service.get_arrears()
		return arrears_list
	except Exception:
		raise HTTPException(status_code=500, detail="Не удалось получить задолженности")
	
	
@router.delete(
	"/{id}",
	status_code=204,
	responses={404:{"description":"Такая задолженность не найдена"},
			   500:{"description":"Не удалось удалить задолженность"}},
	summary="Удалить задолженность"
)
async def delete_arrear(id: int, arrear_service: ArrearServiceDep):
	try:
		await arrear_service.delete_arrear(id)
		return Response(status_code=204)
	except ArrearNotFoundException:
		raise HTTPException(status_code=404, detail="Такая задолженность не найдена")
	except Exception:
		raise HTTPException(status_code=500, detail="Не удалось удалить задолженность")
		



