from sqlalchemy import MetaData, Integer, String, TIMESTAMP, Table, Column, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy import delete as sqlalchemy_delete
from database import Base, db
from sqlalchemy.future import select


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    author = Column(String(200), nullable=False)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"title={self.title}, "
            f")>"
        )

    @classmethod
    async def create(cls, **kwargs):
        book = cls(**kwargs)
        db.add(book)

        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return book

    @classmethod
    async def get_all(cls):
        query = select(cls)
        books = await db.execute(query)
        books = books.scalars().all()
        return books

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )

        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return await cls.get(id)

    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.id == id)
        books = await db.execute(query)
        (book,) = books.first()
        return book

    @classmethod
    async def delete(cls, id):
        query = sqlalchemy_delete(cls).where(cls.id == id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True