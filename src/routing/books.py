from fastapi import APIRouter, HTTPException
from src.schemas import BookUpdateSchema, BookAddSchema, BookSelectSchema
from src.dependencies.books import BookServiceDep
from src.exceptions import BookExistsException, BookNotFoundException
from fastapi import Response, Depends
from src.dependencies.active_user import current_active_user
from fastapi.security import HTTPBearer

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix="/books", tags=["Книги"], dependencies=[Depends(current_active_user), Depends(http_bearer)])

#Ручка создания книги
@router.post(
    "",
    responses={400:{"description": "Такая книга уже существует"},
                500:{"description": "Не удалось добавить книгу"}},
    summary="Добавить книгу",
    response_model=BookSelectSchema
)
async def add_book(data: BookAddSchema, book_service: BookServiceDep)->BookSelectSchema:
    try:
        book_obj = await book_service.add_book(data)
        return book_obj
    except BookExistsException:
        raise HTTPException(status_code=400, detail="Такая книга уже существует")
    except Exception:
        raise HTTPException(status_code=500, detail="Не удалось добавить книгу")

#Ручка получения всех книг	
@router.get(
    "",
    responses={500:{"description":"Не удалось получить книги"}},
    summary="Получить все книги",
    response_model=list[BookSelectSchema]
)
async def get_books(book_service: BookServiceDep)->list[BookSelectSchema]:
    try:
        book_list = await book_service.get_books()
        return book_list
    except Exception:
        raise HTTPException(status_code=500, detail="Не удалось получить книги")


#Ручка получения конкретной книги
@router.get(
    "/{id}",
    responses={404:{"description":"Такая книга не найдена"}},
    summary="Получить книгу по id",
    response_model=BookSelectSchema
)
async def get_book(id: int, book_service: BookServiceDep)->BookSelectSchema:
    try:
        book_obj = await book_service.get_book(id)
        return book_obj
    except BookNotFoundException:
        raise HTTPException(status_code=404, detail="Такая книга не найдена")

#Ручка обновления книги
@router.patch(
    "/{id}",
    responses={404:{"description":"Такая книга не найдена"},
               500:{"description":"Не удалось обновить книгу"}},
    summary="Обновить книгу",
    response_model=BookSelectSchema
)
async def update_book(id: int, data: BookUpdateSchema, book_service: BookServiceDep)->BookSelectSchema:
    try:
        updt_book = await book_service.update_book(id, data)
        return updt_book
    except BookNotFoundException:
        raise HTTPException(status_code=404, detail="Такая книга не найдена")
    except Exception:
        raise HTTPException(status_code=500, detail="Не удалось обновить книгу")

#Ручка удаления книги
@router.delete(
    "/{id}",
    status_code=204,
    responses={404:{"description":"Такая книга не найдена"},
              500:{"description":"Не удалось удалить книгу"}},
    summary="Удалить книгу"
)
async def delete_book(id: int, book_service: BookServiceDep):
    try:
        await book_service.delete_book(id)
        return Response(status_code=204)
    except BookNotFoundException:
        raise HTTPException(status_code=404, detail="Такая книга не найдена")
    except Exception:
        raise HTTPException(status_code=500, detail="Не удалось удалить книгу")
