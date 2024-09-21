from fastapi import FastAPI, HTTPException
from database import Database
from contextlib import asynccontextmanager

app = FastAPI()
db = Database()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    db.close()

app = FastAPI(lifespan=lifespan)

# Fetch all books
@app.get("/api/books")
async def get_books():
    books = db.get_books()
    return {"books": books}

# Add a book (backend endpoint)
@app.post("/api/books")
async def add_book(title: str, author: str, year: int, description: str):
    db.add_book(title, author, year, description)
    return {"message": "Book added successfully"}

# Fetch a single book
@app.get("/api/books/{book_id}")
async def get_book(book_id: int):
    book = db.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"book": book}

# Update a book
@app.put("/api/books/{book_id}")
async def update_book(book_id: int, title: str, author: str, year: int, description: str):
    book = db.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.update_book(book_id, title, author, year, description)
    return {"message": "Book updated successfully"}

# Delete a book
@app.delete("/api/books/{book_id}")
async def delete_book(book_id: int):
    db.delete_book(book_id)
    return {"message": "Book deleted successfully"}
