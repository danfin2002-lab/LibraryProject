from fastapi import APIRouter, HTTPException, Response, Depends
from src.schemas import AuthorAddSchema, AuthorSelectSchema
from src.dependencies.authors import AuthorServiceDep
from src.exceptions import AuthorExistsException, AuthorNotFoundException
from src.dependencies.active_user import current_active_user
from fastapi.security import HTTPBearer

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/authors", tags=["Авторы"], dependencies=[Depends(current_active_user), Depends(http_bearer)])

#Ручка создания автора
@router.post(
		"",
		responses={400:{"descriptions":"Такой автор уже существует"},
				 500:{"descriptions":"Не удалось добавить автора"}},
		summary="Добавить автора",
		response_model=AuthorSelectSchema
	)
async def add_author(data: AuthorAddSchema, author_service: AuthorServiceDep)->AuthorSelectSchema:
	try:
		author_obj = await author_service.add_author(data)
		return author_obj
	except AuthorExistsException:
		raise HTTPException(status_code=400, detail="Такой автор уже существует")
	except Exception:
		raise HTTPException(status_code=500, detail="Не удалось добавить автора")


@router.get(
	"",
    responses={500:{"descriptions":"Не удалось получить авторов"}},
	summary="Получить всех авторов",
	response_model=list[AuthorSelectSchema]
)
async def get_authors(author_service: AuthorServiceDep)->list[AuthorSelectSchema]:
	try:
		author_list = await author_service.get_authors()
		return author_list
	except Exception:
		raise HTTPException(status_code=500, detail="Не удалось получить авторов")

@router.get(
	"/{id}",
	responses={404:{"descriptions":"Такой автор не найден"}},
	summary="Получить автора по id",
	response_model=AuthorSelectSchema
)
async def get_author(id: int, author_service: AuthorServiceDep)->AuthorSelectSchema:
	try:	
		author_obj = await author_service.get_author(id)
		return author_obj
	except AuthorNotFoundException:
		raise HTTPException(status_code=404, detail="Такой автор не найден")

@router.patch(
	"/{id}",
	responses={404:{"descriptions":"Такой автор не найден"},
			   500:{"descriptions":"Не удалось обновить автора"}},
	summary="Обновить информацию об авторе",
	response_model=AuthorSelectSchema
)
async def update_author(id: int, data: AuthorAddSchema, author_service: AuthorServiceDep)->AuthorSelectSchema:
	try:
		updt_author = await author_service.update_author(id, data)
		return updt_author
	except AuthorNotFoundException:
		raise HTTPException(status_code=404, detail="Такой автор не найден")
	except Exception:
		raise HTTPException(status_code=500, detail="Не удалось обновить автора")


@router.delete(
	"/id",
	status_code=204,
	responses={404:{"descriptions":"Такой автор не найден"},
			   500:{"descriptions":"Не удалось удалить автора"}},
	summary="Удалить автора")
async def delete_author(id: int, author_service: AuthorServiceDep):
	try:
		await author_service.delete_author(id)
		return Response(status_code=204)
	except AuthorNotFoundException:
		raise HTTPException(status_code=404, detail="Такой автор не найден")
	except Exception:
		raise HTTPException(status_code=500, detail="Не удалось удалить автора")
