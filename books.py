from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title two", "author": "Author two", "category": "science"},
    {"title": "Title three", "author": "Author three", "category": "history"},
    {"title": "Title four", "author": "Author four", "category": "maths"},
    {"title": "Title five", "author": "Author five", "category": "maths"},
    {"title": "Title six", "author": "Author two", "category": "maths"},
]


@app.get("/books")
async def read_all_books():  # type: ignore
    return BOOKS


@app.get("/books/{book_title}")
async def read_all_books(book_title: str):

    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():  # type: ignore
            return book


@app.get("/books/")
async def read_category_by_query(category: str):
    return [i for i in BOOKS if i.get("category").casefold() == category.casefold()]


@app.get("/books/{book_author}/")
async def read_autor_category_by_query(book_author: str, category: str):

    return [
        i
        for i in BOOKS
        if i.get("author").casefold() == book_author.casefold()
        and i.get("category").casefold() == category.casefold()
    ]


@app.post("/book/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/book/updated_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        print("BOOKS[i]", BOOKS[i])
        if BOOKS[i]["title"].casefold() == updated_book["title"].casefold():
            BOOKS[i] = updated_book
