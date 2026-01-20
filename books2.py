from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status


app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating, published_date):

        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=1900, lt=2100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "aditya",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2012,
            }
        }
    }


BOOKS = [
    Book(1, "Computer Science", "aditya", "Very nice book!", 5, 2012),
    Book(2, "Fast API", "aditya", "Very great book!", 5, 2012),
    Book(3, "Django", "author 1", "ok ok book!", 5, 2022),
    Book(4, "Flask", "author 2", "decent book", 2, 2021),
    Book(5, "Maths", "author 3", "Very nice book!", 3, 2000),
    Book(6, "Maths", "author 4", "Very nice book!", 3, 1997),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Items not found")


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def get_book_by_published_date(published_date: int = Query(gt=1900, lt=2100)):
    return [book for book in BOOKS if book.published_date == published_date]


@app.get("/book/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):

    return [book for book in BOOKS if book.rating == book_rating]


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    print("book request type: ", type(new_book))
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):

    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):

    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book  # type: ignore
            book_changed = True

    if not book_changed:
        raise HTTPException(status_code=404, detail="Items not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):

    book_changed = False
    for i in range(len(BOOKS)):

        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break

    if not book_changed:
        raise HTTPException(status_code=404, detail="Items not found")
