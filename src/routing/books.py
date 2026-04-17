#Мне приходит не автор_нэйм, a автор id
#Сервер должен отловить ошибку, если что не так, а не 500 давать. Нужно обернуть всё в try


from fastapi import APIRouter, HTTPException
from src.schemas import BookUpdateSchema, BookAddSchema, BookSelectSchema
from src.dependencies.repo_serv import BookServiceDep
from src.exceptions import BookExistsException, BookNotFoundException
router = APIRouter(prefix="/books", tags=["Книги"])

#Ручка создания книги
@router.post(
    "",
         responses={400:{"description": "Такая книга уже существует"},
                    500:{"description": "Не удалось добавить книгу"}},
         summary="Добавить книгу"
)
async def add_book(data: BookAddSchema, book_service: BookServiceDep):
    try:
        return await book_service.add_book(data)
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
    summary="Обновить такую книгу",
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
    responses={404:{"description":"Такая книга не найдена"},
              500:{"description":"Не удалось удалить книгу"}},
    summary="Удалить книгу"
)
async def delete_book(id: int, book_service: BookServiceDep):
    try:
        return await book_service.delete_book(id)
    except BookNotFoundException:
        raise HTTPException(status_code=404, detail="Такая книга не найдена")
    except Exception:
        raise HTTPException(status_code=500, detail="Не удалось удалить книгу")
