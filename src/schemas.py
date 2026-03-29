from pydantic import BaseModel, Field
import datetime

class AuthorAddSchema(BaseModel):
	name: str = Field(..., max_length=30)

class AuthorSchema(AuthorAddSchema):
	id: int

class BookSchema(BaseModel):
	title: str
	genre: str
class BookAddSchema(BookSchema):
	author_name: str

class BookSelectSchema(BookSchema):
	id: int
	author_id: int = Field(..., ge=0)

class VisitorAddSchema(BaseModel):
	name: str = Field(..., max_length=30)
	birthday: datetime.date
class VisitorSchema(VisitorAddSchema):
	id: int
class LibraryAddSchema(BaseModel):
	address: str
class LibrarySchema(LibraryAddSchema):
	id: int
class BLAddSchema(BaseModel):
	book_id: int = Field(..., ge=0)
	library_id: int = Field(..., ge=0)
	count: int = Field(..., ge=0, le=1000)
class BLSchema(BLAddSchema):
	id: int
class ArrearAddSchema(BaseModel):
	visitor_id: int = Field(..., ge=0)
	library_id: int = Field(..., ge=0)
	book_id: int = Field(..., ge=0)
class ArrearSchema(ArrearAddSchema):
	id: int
