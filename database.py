from config import DB_NAME, DB_PASS, DB_USER, DB_PORT, DB_HOST
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

Base = declarative_base()


class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self):
        self._engine = create_async_engine(
            DATABASE_URL,
            future=True,
            echo=True,
        )
        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


db = AsyncDatabaseSession()

# Base: DeclarativeMeta = declarative_base()
# engine = create_async_engine(DATABASE_URL, echo=True)
# async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
#
#
# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session
