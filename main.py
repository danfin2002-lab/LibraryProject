import uvicorn
# from src.routing import routers
from fastapi import FastAPI
from src.routing import routers


app = FastAPI()

for router in routers:
	app.include_router(router)

if __name__ == "__main__":
	uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)#reload важен для скорости разработки: сохранили файл - сразу увидели изменения
#host="0.0.0.0" - чтобы приложение было доступно извне контейнера
#host="127.0.0.1" - не позволит зайти по такому ip