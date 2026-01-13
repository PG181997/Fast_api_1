from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {'title' : 'Title One', 'author' : 'Author One', 'category' : 'science'},
    {'title' : 'Title two', 'author' : 'Author two', 'category' : 'science'},
    {'title' : 'Title three', 'author' : 'Author three', 'category' : 'history'},
    {'title' : 'Title four', 'author' : 'Author four', 'category' : 'maths'},
    {'title' : 'Title five', 'author' : 'Author five', 'category' : 'maths'},
    {'title' : 'Title six', 'author' : 'Author two', 'category' : 'maths'},
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_title}")
async def read_all_books(book_title:str):
    
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

