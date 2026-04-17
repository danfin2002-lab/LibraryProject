from src.repositories.libraries import LibraryRepository
from src.schemas import LibraryAddSchema, LibrarySelectSchema
from fastapi import HTTPException
from src.exceptions import LibraryExistsException, LibraryNotFoundException

class LibraryService:
    def __init__(self, repository: LibraryRepository):
        self.repository = repository

    async def add_library(self, data: LibraryAddSchema):
        await self.check_library(data)
        await self.repository.add_library(data)
        return {"ok": "Библиотека успешно добавлена"}

    async def check_library(self, data:LibraryAddSchema):
        existing_library = await self.repository.check_library(data)
        if existing_library is not None:
            raise LibraryExistsException("Такая библиотека уже существует")

    async def get_library(self, id: int)->LibrarySelectSchema:
        library_object = await self.repository.get_library(id)
        if library_object is None:
            raise LibraryNotFoundException("Такая библиотека не найдена")
        return library_object


    async def get_libraries(self)->list[LibrarySelectSchema]:
        library_list = await self.repository.get_libraries()
        return library_list

    async def update_library(self, id: int, data: LibraryAddSchema)->LibrarySelectSchema:
        library_obj = await self.get_library(id)
        updt_library = await self.repository.update_library(data, library_obj)
        return updt_library

    async def delete_library(self, id: int):
        library_obj = await self.get_library(id)
        await self.repository.delete_library(library_obj)
        return {"ok": "Библиотека успешно удалена"}

