from typing import List
from .schemas import BookName, BookCreate, BookBase
from fastapi import APIRouter
from .models import Book
from pydantic import BaseModel

api = APIRouter(
    prefix="/books",
)


# class BookBase(BaseModel):
#     title: str
#     author: str
#
#
# class BookCreate(BookBase):
#     pass
#
#
# class BookName(BookBase):
#     id: int
#
#     class Config:
#         orm_mode = True


@api.post("/", response_model=BookName)
async def create_book(book: BookCreate):
    book = await Book.create(**book.dict())
    return book


@api.get("/{id}", response_model=BookName)
async def get_book(id: int):
    book = await Book.get(id)
    return book


@api.get("/", response_model=List[BookName])
async def get_all_books():
    books = await Book.get_all()
    return books


@api.put("/{id}", response_model=BookName)
async def update(id: int, book: BookBase):
    book = await Book.update(id, **book.dict())
    return book


@api.delete("/{id}", response_model=bool)
async def delete_user(id: int):
    return await Book.delete(id)
