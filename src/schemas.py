from pydantic import BaseModel, Field, ConfigDict
import datetime
from typing import Optional
import uuid
from fastapi_users import schemas



class AuthorAddSchema(BaseModel):
    name: str = Field(..., max_length=30)

class AuthorSelectSchema(AuthorAddSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BookUpdateSchema(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
class BookAddSchema(BaseModel):
    author_id: int = Field(..., ge=0)
    title: str
    genre: str
class BookSelectSchema(BookAddSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class VisitorAddSchema(BaseModel):
    name: str = Field(..., max_length=30)
    birthday: datetime.date
class VisitorSelectSchema(VisitorAddSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class LibraryAddSchema(BaseModel):
    address: str
class LibrarySelectSchema(LibraryAddSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BLAddSchema(BaseModel):
    book_id: int = Field(..., ge=0)
    library_id: int = Field(..., ge=0)
    count: int = Field(..., ge=0, le=1000)
class BLSelectSchema(BLAddSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ArrearAddSchema(BaseModel):
    visitor_id: int = Field(..., ge=0)
    library_id: int = Field(..., ge=0)
    book_id: int = Field(..., ge=0)
class ArrearSelectSchema(ArrearAddSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass
