from fastapi.security import HTTPBearer
from src.authentication.FastAPIUsers import fastapi_users
from src.authentication.backend import auth_backend
from src.schemas import UserCreate, UserRead
from fastapi import APIRouter, Depends

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
	dependencies=[Depends(http_bearer)],
)


router.include_router(
	fastapi_users.get_auth_router(auth_backend),
	prefix="/auth/jwt",
	tags = ["Auth"]
)

router.include_router(
	fastapi_users.get_register_router(UserRead, UserCreate),
	prefix="/auth",
    tags=["Auth"]
)