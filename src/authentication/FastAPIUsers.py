import uuid
from fastapi_users import FastAPIUsers
from src.models import User
from src.authentication.backend import auth_backend
from src.dependencies.users import get_user_manager

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)