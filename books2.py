from fastapi import FastAPI

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
