from fastapi import APIRouter, HTTPException
from src.schemas import BLAddSchema, BLSelectSchema
from src.dependencies.repo_serv import  BLServiceDep
from src.exceptions import BLNotFoundException

router = APIRouter(prefix="/book-library", tags=["Книги библиотек"])


@router.post(
    "",
    responses={500:{"description": "Не удалось добавить книгу в бибилотеку"}},
    summary="Добавить книгу в данную библиотеку"
)
async def add_Bl(data: BLAddSchema, bl_service: BLServiceDep):
    try:
        return await bl_service.add_BL(data)
    except Exception:
        raise HTTPException(status_code=500, detail="Не удалось добавить книгу в бибилотеку")

@router.get(
    "",
    responses={500: {"description":"Не удалось получить книги из библиотек"}},
    summary="Получить все книги библиотек",
    response_model=list[BLSelectSchema]
)
async def get_BLs(bl_service: BLServiceDep)->list[BLSelectSchema]:
    try:
        bl_list = await bl_service.get_BLs()
        return bl_list
    except Exception:
        raise HTTPException(status_code=500, detail="Не удалось получить книги в библиотек")

@router.get(
    "/{id}",
    responses={404:{"description":"Такой связи книга-библиотека нет"}},
    summary="Получить связь книги и бибилиотеки",
    response_model=BLSelectSchema
)
async def get_BL(id: int, bl_service: BLServiceDep)->BLSelectSchema:
    try:
        bl_obj = await bl_service.get_BL(id)
        return bl_obj
    except BLNotFoundException:
        raise HTTPException(status_code=404, detail="Такой связи книга-библиотека нет")

@router.delete(
    "/{id}",
    responses={404:{"description":"Такой связи книга-библиотека нет"},
              500:{"description":"Не удалось удалить книгу из библиотеки"}},
    summary="Удалить книгу в библиотеке"
)
async def delete_BL(id: int, bl_service: BLServiceDep):
    try:
        return await bl_service.delete_BL(id)
    except BLNotFoundException:
        raise HTTPException(status_code=404, detail="Такой связи книга-библиотека нет")
    except Exception:
        raise HTTPException(status_code=500, detail="Не удалось удалить книгу из библиотеки")