from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine, URL, text, engine
from sqlalchemy.ext.asyncio import create_async_engine, async_session, async_sessionmaker, AsyncSession

from src.config import settings
from sqlalchemy.orm import sessionmaker, Session

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True
)
async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True
)

sync_session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)
#
# async def get_async_session():
#     async with async_session_factory() as session:
#         yield session
#
# SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

# with sync_engine.connect() as conn:
#      res = conn.execute(text("SELECT 123 union select 456"))
#      print(f"{res.first()=}")
