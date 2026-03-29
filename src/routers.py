from .models import Author, Book, Visitor, Library, BL, Arrear
from fastapi import HTTPException, APIRouter
from sqlalchemy import select
from .schemas import  AuthorSchema,AuthorAddSchema,BookSchema,BookAddSchema,LibrarySchema,LibraryAddSchema,BookSelectSchema,VisitorSchema,VisitorAddSchema,BLSchema,BLAddSchema,ArrearSchema,ArrearAddSchema
from .dependencies import SessionDep
router = APIRouter()
@router.post("/authors", tags=["Авторы"], summary="Добавить автора")
async def add_author(data: AuthorAddSchema, session: SessionDep):
	#Проверка, есть ли уже такой автор
	existing_author = await session.scalar(
	select(Author).where(Author.name == data.name)
	)
	if existing_author is None:
		new_author = Author(
		name = data.name
		)
		session.add(new_author)
		await session.commit()
		return {"ok": "Автор добавлен"}

	raise HTTPException(
	status_code=400,
	detail="Такой автор уже существует"
	)

@router.get("/authors", tags=["Авторы"], summary="Получить авторов")
async def get_authors(session: SessionDep)->list[AuthorSchema]:
	#query = select(Author) #Это через ORM
	#result = await session.execute(query)
	#return result.scalars().all()
	authors_list = (await session.scalars(select(Author))).all()
	if not authors_list:
		raise HTTPException(
		status_code=404,
		detail="Авторы не найдены"
		)
	return authors_list

@router.get("/authors/{author_id}", tags=["Авторы"], summary="Получить автора")
async def get_author(author_id: int, session: SessionDep)->AuthorSchema:
	author_obj = await session.get(Author, author_id)
	if author_obj is None:
		raise HTTPException(
		status_code=404,
		detail="Не удалось найти автора"
		)
	return author_obj
	# query = select(Author) #Это через ORM
	# result = await session.execute(query)
	# return result.scalars().all()

@router.patch("/authors/{author_id}",tags=["Авторы"], summary="Обновить информацию об авторе")
async def update_author(author_id: int, data: AuthorAddSchema, session: SessionDep):
	author_obj = await session.get(Author, author_id)
	if author_obj is None:
		raise HTTPException(
		status_code=404,
		detail="Не удалось найти автора"
		)
	author_obj.name = data.name # Опять в сессию мы ничего не добаляем, так этот объект и так есть в этой сессии, потому что именно оттуда мы его и получили
	await session.commit()
	return {"ok": "Автор успешно обновлён"}


@router.delete("/authors/{author_id}", tags=["Авторы"], summary="Удалить автора")
async def delete_author(author_id: int, session: SessionDep):
	author_obj = await session.get(Author, author_id)
	if author_obj is None:
		raise HTTPException(
		status_code=404,
		detail="Не удалось найти автора"
		)
	await session.delete(author_obj)
	await session.commit()
	return {"ok": "Автор успешно удалён"}


@router.post("/books", tags = ["Книги"], summary =  "Добавить книгу")
async def add_book(data: BookAddSchema, session: SessionDep):
	author_obj = await session.scalar(
		select(Author).where(Author.name == data.author_name)
	)
	if author_obj is None:
		raise HTTPException(
		status_code=404,
		detail="Автора этой книги не существует"
		)
	#Добавить проверку, есть ли уже такая книга
	existing_book = await session.scalar(select(Book).where(Book.title == data.title, Book.genre == data.genre, Book.author_id == author_obj.id))
	if existing_book is None:
		book_obj = Book(
			title = data.title,
			genre = data.genre,
			author_id = author_obj.id
		)
		session.add(book_obj)
		await session.commit()
		return {"ok": "Книга добавлена"}
	raise HTTPException(
	status_code=400,
	detail="Такая книга уже существует"
	)

@router.get("/books/{book_title}", tags=["Книги"], summary="Получить книгу по названию")
async def get_book_by_title(book_title: str, session:SessionDep)->BookSelectSchema:
	book_obj = await session.scalar(
		select(Book).where(Book.title == book_title)
	)
	if book_obj is None:
		raise HTTPException(
		status_code=404,
		detail="Такая книга не найдена"
		)
	return book_obj

@router.get("/books", tags=["Книги"], summary="Получить все книги")
async def get_books(session: SessionDep)->list[BookSelectSchema]:
	#!!!
	#query = select(Book)
	book_list = (await session.scalars(select(Book))).all()
	if not book_list:
		raise HTTPException(
		status_code=404,
		detail="Книги не найдены"
		)
	return book_list

@router.patch("/books/{book_title}",tags=["Книги"], summary="Обновить книгу с таким названием" )
async def update_book(book_title: str, data:BookSchema, session:SessionDep):
	#query = select(Book).where(Book.title == book_title)
	#book_res = await session.execute(query)
	#book_obj = book_res.scalar()
	book_obj = await session.scalar(
	select(Book).where(Book.title == book_title)
	)
	if book_obj is None:
		raise HTTPException(
		status_code=404,
		detail="Такая книга не найдена"
		)
	print("//////////////////////")
	print(book_obj)
	print("//////////////////////")
	book_obj.title = data.title
	book_obj.genre = data.genre

	await session.commit()

	return {"Ok": "Книга обновлена"}

@router.delete("/books/{book_title}", tags=["Книги"], summary="Удалить книгу с таким названием")
async def delete_book(book_title: str, session: SessionDep):
	book_obj = await session.scalar(select(Book).where(Book.title==book_title))
	if book_obj is None:
		raise HTTPException(
			status_code=404,
			detail="Такая книга не найдена"
		)

	await session.delete(book_obj)
	await session.commit()
	return {"Ok": "Книга успешно удалена"}

@router.post("/visitors", tags = ["Посетители"], summary="Создать посетителя")
async def add_visitor(data: VisitorAddSchema, session: SessionDep):
	existing_visitor = await session.scalar(
		select(Visitor).where(
			Visitor.name == data.name, Visitor.birthday == data.birthday
		)
	)
	if existing_visitor is not None:
		raise HTTPException(status_code=400, detail="Такой посетитель уже есть")

	visitor_obj = Visitor(
		name = data.name,
		birthday = data.birthday
	)
	session.add(visitor_obj)
	await session.commit()
	return {"Ok": "Посетитель успешно добавлен"}

@router.delete("/visitors/{visitor_name}", tags = ["Посетители"], summary="Удалить посетителя")
async def delete_visitor(visitor_name: str, session: SessionDep):
	visitor_obj = await session.scalar(select(Visitor).where(Visitor.name == visitor_name))

	if visitor_obj is None:
		raise HTTPException(status_code=404, detail="Такого посетителя нет")

	await session.delete(visitor_obj)
	await session.commit()
	return {"Ok": "Посетитель успешно удалён"}

@router.get("/visitors", tags = ["Посетители"], summary="Получить всех посетителей")
async def get_visitors(session: SessionDep)->list[VisitorSchema]:
	visitors_list = (await session.scalars(select(Visitor))).all()
	if not visitors_list:
		raise HTTPException(status_code=404, detail="Посетители не найдены")
	return visitors_list

@router.get("/visitors/{visitor_name}", tags = ["Посетители"], summary="Получить посетителя по имени")
async def get_visitor_by_name(visitor_name: str, session:SessionDep)->VisitorSchema:
	visitor_obj = await session.scalar(select(Visitor).where(Visitor.name == visitor_name))
	if visitor_obj is None:
		raise HTTPException(status_code=404, detail="Посетитель с таким именем не найден")
	return visitor_obj

@router.patch("/visitors/{visitor_name}", tags = ["Посетители"], summary="Изменить данные посетителя по имени")
async def update_visitor(visitor_name: str, data:VisitorAddSchema, session:SessionDep):
	visitor_obj = await session.scalar(select(Visitor).where(Visitor.name == visitor_name))
	if visitor_obj is None:
		raise HTTPException(status_code=404, detail="Посетитель с таким именем не найден")

	visitor_obj.name = data.name
	visitor_obj.birthday = data.birthday

	await session.commit()
	return {"ok": "Посетитель успешно обновлён"}

@router.post("/libraries", tags=["Библиотеки"], summary="Создать новую библиотеку")
async def create_library(data: LibraryAddSchema, session:SessionDep):
	existing_library = await session.scalar(
		select(Library).where
		(Library.address == data.address)
	)
	if existing_library is not None:
		raise HTTPException(status_code=400, detail="Такая библиотека уже есть")
	library_object = Library(
		address = data.address
	)
	session.add(library_object)
	await session.commit()

	return {"Ok": f"Библиотека по адресу {library_object.address} успешно добавлена"}

@router.get("/libraries/{library_id}", tags=["Библиотеки"], summary="Получить библиотеку по id")
async def get_library(library_id: int, session:SessionDep)->LibrarySchema:
	library_object = await session.get(Library, library_id)
	if library_object is None:
		raise HTTPException(status_code=400, detail="Такая библиотека не найдена")
	return library_object

@router.get("/libraries", tags=["Библиотеки"], summary="Получить все библиотеки")
async def get_libraries(session:SessionDep)->list[LibrarySchema]:
	libraries_list = (await session.scalars(select(Library))).all()
	if not libraries_list:
		raise HTTPException(status_code=404, detail="Библиотеки не найдены")
	return libraries_list

@router.delete("/libraries/{library_id}", tags=["Библиотеки"], summary="Удалить библиотеку")
async def delete_library(library_id: int, session: SessionDep):
	library_obj = await session.get(Library, library_id)
	if library_obj is None:
		raise HTTPException(status_code=404, detail="Такая библиотека не найдена")
	await session.delete(library_obj)
	await session.commit()
	return {"Ok", f"Библиотека с id = {library_id} удалена"}

@router.patch("/libraries/{library_id}", tags=["Библиотеки"], summary="Изменить данные о библиотеке")
async def update_library(library_id: int, data: LibraryAddSchema, session: SessionDep):
	library_obj = await session.get(Library, library_id)
	if library_obj is None:
		raise HTTPException(status_code=404, detail="Такая библиотека не найдена")
	library_obj.address = data.address
	await session.commit()
	return {"ok": "Библиотека успешно обновлена"}

@router.post("/book-library", tags=["Книги библиотек"], summary="Добавить книгу в данную библиотеку")
async def create_bl(data: BLAddSchema, session:SessionDep):
	# Если такая книга у такой библиотеки есть, то  count нужно просто прибавить.
	# Но двух одинаков library_id и book_id одновременно быть не должно

	#Проверка, есть ли уже такая связь
	existing_BL = await session.scalar(
	select(BL).where(BL.book_id == data.book_id,
	BL.library_id == data.library_id
		)
	)

	if existing_BL is None:
		BL_obj = BL(
			book_id = data.book_id,
			library_id = data.library_id,
			count = data.count
		)
		session.add(BL_obj)
	else:
		existing_BL.count += data.count
		if existing_BL.count > 1000:
			existing_BL.count = 1000


	await session.commit()
	return {"Ok": f"Книга успешно добавлена в библиотеку"}

@router.delete("/book-library/{bl_id}", tags=["Книги библиотек"], summary="Удалить такую книгу из этой библиотеки")
async def delete_bl(bl_id: int, session: SessionDep):
	BL_obj = await session.get(BL, bl_id)
	if BL_obj is None:
		raise HTTPException(status_code=404, detail="Такая связь не найдена")
	await session.delete(BL_obj)
	#Если связь книга-библиотека удаляется, то и задолженности такие надо удалить
	arrears_list = (await session.scalars(select(Arrear).where(Arrear.book_id == BL_obj.book_id, Arrear.library_id == BL_obj.library_id))).all()
	for arrear in arrears_list:
		await session.delete(arrear)
	await session.commit()
	return {"Ok": f"Связь успешно удалена"}

@router.get("/book-library", tags=["Книги библиотек"], summary="Получить все книги из всех библиотек")
async def get_BL(session:SessionDep)->list[BLSchema]:
	BL_list = (await session.scalars(select(BL))).all()
	if not BL_list:
		raise HTTPException(status_code=404, detail="Связи не найдены")

	return BL_list

@router.get("/book-library/by-book/{book_id}", tags=["Книги библиотек"], summary="Получить все библиотеки, имеющие книгу с таким id")
async def get_BL_by_book_id(book_id: int, session: SessionDep)->list[BLSchema]:
	BL_list = (await session.scalars(select(BL).where(BL.book_id == book_id))).all()
	if not BL_list:
		raise HTTPException(status_code=404, detail="Связи не найдены")
	return BL_list

@router.get("/book-library/by-library/{library_id}", tags=["Книги библиотек"], summary="Получить все книги, которые находятся в библиотеке с таким id")
async def get_BL_by_book_id(library_id: int, session: SessionDep)->list[BLSchema]:
	BL_list = (await session.scalars(select(BL).where(BL.library_id == library_id))).all()
	if not BL_list:
		raise HTTPException(status_code=404, detail="Связи не найдены")
	return BL_list


@router.post("/arrears", tags=["Задолженности"], summary="Добавить задолженность")
async def add_arrear(data: ArrearAddSchema, session:SessionDep):
	#Проверка, есть ли такой пользователь в БД
	visitor_obj = await session.get(Visitor, data.visitor_id)
	if visitor_obj is None:
		raise HTTPException(
		status_code=404,
		detail="Такой посетитель не найден"
		)
	#Проверка, существует ли такая связь между книгой и библиотекой в BL
	bl_obj = await session.scalar(
	select(BL).where(
			BL.book_id == data.book_id,
			BL.library_id == data.library_id
		)
	)
	if not bl_obj:
		raise HTTPException(
		status_code=404,
		detail="Такая связь книга-библиотека не найдена"
		)
	#Нужно корректировать count

	if bl_obj.count > 0:
		arrear_obj = Arrear(
		book_id = data.book_id,
		library_id = data.library_id,
		visitor_id = data.visitor_id
		)
		session.add(arrear_obj)
		bl_obj.count -= 1
		await session.commit()
		return {"Ok": "Новая задолженность добавлена"}
	else:
		return  {"Message": "В библиотеке не хватает таких книг"}


@router.get("/arrears", tags=["Задолженности"], summary="Получить все задолженности")
async def get_arrears(session:SessionDep)->list[ArrearSchema]:
	#Возможно, стоит сделать по-старинке
	arrears_list = (await session.scalars(select(Arrear))).all()
	if not arrears_list:
		raise HTTPException(status_code=404, detail="Задолженности не найдены")
	return arrears_list

@router.get("/arrears/by_library/{library_id}", tags=["Задолженности"], summary="Получить все задолженности для этой библиотеки")
async def get_arrears_by_library(library_id: int, session:SessionDep)->list[ArrearSchema]:
	library_obj = await session.get(Library, library_id)
	if library_obj is None:
		raise HTTPException(
		status_code=404,
		detail="Такой библиотеки не существует"
	)
	arrears_list = (await session.scalars(select(Arrear).where(Arrear.library_id==library_id))).all()
	if arrears_list is None:
		raise HTTPException(status_code=404, detail="Задолженности не найдены")
	return arrears_list

@router.get("/arrears/by_book/{book_id}", tags=["Задолженности"], summary="Получить все задолженности по этой книге")
async def get_arrears_by_book(book_id: int, session:SessionDep)->list[ArrearSchema]:
	book_obj = await session.get(Book, book_id)
	if book_obj is None:
		raise HTTPException(
		status_code=404,
		detail="Такой книги не существует"
	)
	arrears_list = (await session.scalars(select(Arrear).where(Arrear.book_id==book_id))).all()
	if arrears_list is None:
		raise HTTPException(status_code=404, detail="Задолженности не найдены")
	return arrears_list

@router.get("/arrears/by_visitor/{visitor_id}", tags=["Задолженности"], summary="Получить все задолженности данного посетителя")
async def get_arrears_by_visitor(visitor_id: int, session:SessionDep)->list[ArrearSchema]:
	visitor_obj = await session.get(Visitor, visitor_id)
	if visitor_obj is None:
		raise HTTPException(
		status_code=404,
		detail="Такого посетителя не существует"
	)
	arrears_list = (await session.scalars(select(Arrear).where(Arrear.visitor_id==visitor_id))).all()
	if arrears_list is None:
		raise HTTPException(status_code=404, detail="Задолженности не найдены")
	return arrears_list


@router.delete("/arrears/{id}", tags=["Задолженности"], summary="Удалить данную задолженность")
async def delete_arrear(id: int, session: SessionDep):
	#Проверить, есть ли в принципе такая задолженность
	arrear_obj = await session.get(Arrear, id)
	#Да - удаляем, нет - возвращаем ошибку
	if arrear_obj is None:
		raise HTTPException(
		status_code=404,
		detail="Такой задолженности не существует"
	)
	await session.delete(arrear_obj)
	#Добавляем в count записи BL, где совпадают book_id, library_id
	bl_obj = await session.scalar(
	select(BL).where(BL.book_id == arrear_obj.book_id,
		BL.library_id == arrear_obj.library_id)
	)
	bl_obj.count += 1


	await session.commit()
	return {"Ok": f"Задолженность успешно удалена"}
