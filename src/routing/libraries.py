from fastapi import APIRouter, HTTPException, Response, Depends
from src.schemas import LibraryAddSchema, LibrarySelectSchema
from src.dependencies.libraries import LibraryServiceDep
from src.exceptions import LibraryExistsException, LibraryNotFoundException
from src.dependencies.active_user import current_active_user
from fastapi.security import HTTPBearer

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix="/libraries", tags=["Библиотеки"], dependencies=[Depends(current_active_user), Depends(http_bearer)])


# Ручка создания библиотеки
@router.post(
    "",
    responses={400: {"description": "Такая библиотека уже существует"},
               500: {"description": "Не удалось добавить библиотеку"}},
    summary="Добавить библиотеку",
    response_model=LibrarySelectSchema
)
async def add_library(data: LibraryAddSchema, library_service: LibraryServiceDep)->LibrarySelectSchema:
    try:
        library_obj = await library_service.add_library(data)
        return library_obj
    except LibraryExistsException:
        raise HTTPException(status_code=400, detail="Такая библиотека уже существует")
    except Exception:
        raise HTTPException(status_code=500, detail="Не удалось добавить библиотеку")


# Ручка получения всех библиотек
@router.get(
    "",
    responses={500: {"description": "Не удалось получить библиотеки"}},
    summary="Получить все библиотеки",
    response_model=list[LibrarySelectSchema]
)
async def get_libraries(library_service: LibraryServiceDep) -> list[LibrarySelectSchema]:
    try:
        library_list = await library_service.get_libraries()
        return library_list
    except Exception:
        raise HTTPException(status_code=500, detail="Не удалось получить библиотеки")


# Ручка получения конкретной библиотеки
@router.get(
    "/{id}",
    responses={404: {"description": "Такая библиотека не найдена"}},
    summary="Получить библиотеку по id",
    response_model=LibrarySelectSchema
)
async def get_library(id: int, library_service: LibraryServiceDep) -> LibrarySelectSchema:
    try:
        library_obj = await library_service.get_library(id)
        return library_obj
    except LibraryNotFoundException:
        raise HTTPException(status_code=404, detail="Такая библиотека не найдена")


# Ручка обновления библиотеки
@router.patch(
    "/{id}",
    responses={404: {"description": "Такая библиотека не найдена"},
               500: {"description": "Не удалось обновить библиотеку"}},
    summary="Обновить библиотеку",
    response_model=LibrarySelectSchema
)
async def update_library(id: int, data: LibraryAddSchema, library_service: LibraryServiceDep) -> LibrarySelectSchema:
    try:
        updt_library = await library_service.update_library(id, data)
        return updt_library
    except LibraryNotFoundException:
        raise HTTPException(status_code=404, detail="Такая библиотека не найдена")
    except Exception:
        raise HTTPException(status_code=500, detail="Не удалось обновить библиотеку")


# Ручка удаления библиотеки
@router.delete(
    "/{id}",
    status_code=204,
    responses={404: {"description": "Такая библиотека не найдена"},
               500: {"description": "Не удалось удалить библиотеку"}},
    summary="Удалить библиотеку"
)
async def delete_library(id: int, library_service: LibraryServiceDep):
    try:
        await library_service.delete_library(id)
        return Response(status_code=204)
    except LibraryNotFoundException:
        raise HTTPException(status_code=404, detail="Такая библиотека не найдена")
    except Exception:
        raise HTTPException(status_code=500, detail="Не удалось удалить библиотеку")
