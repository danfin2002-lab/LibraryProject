from fastapi import APIRouter, Depends
from src.schemas import UserRead, UserUpdate
from src.authentication.FastAPIUsers import fastapi_users
from fastapi.security import HTTPBearer

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
	dependencies=[Depends(http_bearer)],
)

#Юзера мы получаем либо по
#"/me"
# либо "/{id}"
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)