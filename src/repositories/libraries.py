from src.dependencies.session import SessionDep
from src.schemas import LibraryAddSchema, LibrarySelectSchema
from sqlalchemy import select
from src.models import Library

class LibraryRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    #check_library
    async def check_library(self, data:LibraryAddSchema)->LibrarySelectSchema:
        existing_library = await self.session.scalar(
            select(Library).where
            (Library.address == data.address)
        )
        return existing_library
    #add_library
    async def add_library(self, data:LibraryAddSchema):
        library_object = Library(
            address = data.address
        )
        self.session.add(library_object)
        await self.session.commit()

    #get_library
    async def get_library(self, id: int)->LibrarySelectSchema:
        library_object = await self.session.get(Library, id)
        return library_object
    #get_libraries
    async def get_libraries(self)->list[LibrarySelectSchema]:
        libraries_list = (await self.session.scalars(select(Library))).all()
        return libraries_list
    #update_library
    async def update_library(self, data: LibraryAddSchema, library_obj: LibrarySelectSchema)->LibrarySelectSchema:
        if data.address is not None:
            library_obj.address = data.address

        await self.session.commit()
        return library_obj
    #delete_library
    async def delete_library(self, library_obj: LibrarySelectSchema):
        await self.session.delete(library_obj)
        await self.session.commit()
