from src.dependencies.session import SessionDep
from src.schemas import LibraryAddSchema, LibrarySelectSchema
from sqlalchemy import select
from src.models import Library

class LibraryRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    #check_library
    async def check_library(self, data:LibraryAddSchema)->Library:
        existing_library = await self.session.scalar(
            select(Library).where
            (Library.address == data.address)
        )
        return existing_library
    #add_library
    async def add_library(self, data:LibraryAddSchema)->Library:
        library_object = Library(
            address = data.address
        )
        self.session.add(library_object)
        await self.session.commit()
        return library_object

    #get_library
    async def get_library(self, id: int)->Library:
        library_object = await self.session.get(Library, id)
        return library_object
    #get_libraries
    async def get_libraries(self)->list[Library]:
        libraries_list = (await self.session.scalars(select(Library))).all()
        return libraries_list
    #update_library
    async def update_library(self, data: LibraryAddSchema, library_obj: Library)->Library:
        #if data.address is not None:
        #    library_obj.address = data.address

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(library_obj, key, value)

        await self.session.commit()
        return library_obj

    #delete_library
    async def delete_library(self, library_obj: Library):
        await self.session.delete(library_obj)
        await self.session.commit()
