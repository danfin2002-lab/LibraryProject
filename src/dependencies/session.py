from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_factory

async def get_async_session():
    async with async_session_factory() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]