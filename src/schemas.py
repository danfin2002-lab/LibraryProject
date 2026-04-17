from pydantic import BaseModel, Field
import datetime
from typing import Optional

class AuthorAddSchema(BaseModel):
	name: str = Field(..., max_length=30)

class AuthorSelectSchema(AuthorAddSchema):
	id: int
	

class BookUpdateSchema(BaseModel):
	title: Optional[str] = None
	genre: Optional[str] = None
class BookAddSchema(BaseModel):
	author_id: int = Field(..., ge=0)
	title: str
	genre: str
class BookSelectSchema(BookAddSchema):
	id: int


class VisitorAddSchema(BaseModel):
	name: str = Field(..., max_length=30)
	birthday: datetime.date
class VisitorSelectSchema(VisitorAddSchema):
	id: int


class LibraryAddSchema(BaseModel):
	address: str
class LibrarySelectSchema(LibraryAddSchema):
	id: int


class BLAddSchema(BaseModel):
	book_id: int = Field(..., ge=0)
	library_id: int = Field(..., ge=0)
	count: int = Field(..., ge=0, le=1000)
class BLSelectSchema(BLAddSchema):
	id: int
	
	
class ArrearAddSchema(BaseModel):
	visitor_id: int = Field(..., ge=0)
	library_id: int = Field(..., ge=0)
	book_id: int = Field(..., ge=0)
class ArrearSelectSchema(ArrearAddSchema):
	id: int
