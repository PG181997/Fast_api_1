from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):

        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    
    model_config = {
        "json_schema_extra" : {
            "example" : {
                "title" : "A new book",
                "author" : "aditya",
                "description" : "A new description of a book",
                "rating" : 5
            }
        }
    }


BOOKS = [
    Book(1, "Computer Science", "aditya", "Very nice book!", 5),
    Book(2, "Fast API", "aditya", "Very great book!", 5),
    Book(3, "Django", "author 1", "ok ok book!", 5),
    Book(4, "Flask", "author 2", "decent book", 2),
    Book(5, "Maths", "author 3", "Very nice book!", 1.5),
    Book(6, "Maths", "author 4", "Very nice book!", 0.5),
]


@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}")
async def read_book(book_id:int):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    print("book request type: ", type(new_book))
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):

    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
