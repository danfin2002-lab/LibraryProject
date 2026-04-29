from fastapi import Depends
from src.models import User
from src.authentication.user_manager import UserManager
from src.dependencies.session import SessionDep
from fastapi_users.db import SQLAlchemyUserDatabase

async def get_user_db(session: SessionDep):
    return SQLAlchemyUserDatabase(session, User)

async def get_user_manager(user_db=Depends(get_user_db)):
    return UserManager(user_db)