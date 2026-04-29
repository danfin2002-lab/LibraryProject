from src.repositories.libraries import LibraryRepository
from src.schemas import LibraryAddSchema
from fastapi import HTTPException
from src.exceptions import LibraryExistsException, LibraryNotFoundException
from src.models import Library

class LibraryService:
    def __init__(self, repository: LibraryRepository):
        self.repository = repository

    async def add_library(self, data: LibraryAddSchema)->Library:
        await self.check_library(data)
        library_obj = await self.repository.add_library(data)
        return library_obj
		
    async def check_library(self, data: LibraryAddSchema):
        existing_library = await self.repository.check_library(data)
        if existing_library is not None:
            raise LibraryExistsException("Такая библиотека уже существует")

    async def get_library(self, id: int)->Library:
        library_object = await self.repository.get_library(id)
        if library_object is None:
            raise LibraryNotFoundException("Такая библиотека не найдена")
        return library_object

    async def get_libraries(self)->list[Library]:
        library_list = await self.repository.get_libraries()
        return library_list

    async def update_library(self, id: int, data: LibraryAddSchema)->Library:
        library_obj = await self.get_library(id)
        updt_library = await self.repository.update_library(data, library_obj)
        return updt_library

    async def delete_library(self, id: int):
        library_obj = await self.get_library(id)
        await self.repository.delete_library(library_obj)

