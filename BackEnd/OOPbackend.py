from fastapi import FastAPI, HTTPException
from database import Database
from models import Book
from contextlib import asynccontextmanager

app = FastAPI()
db = Database()

@asynccontextmanager
async def lifespan():
    yield
    db.close()

# Fetch all books
@app.get("/api/books")
async def get_books():
    books = db.get_books()
    return [{"id": row[0], "title": row[1], "author": row[2], "year": row[3], "description": row[4]} for row in books]

#    return {"books": books}

# Add a book (backend endpoint)
@app.post("/api/books")
async def add_book(book: Book):
    db.add_book(book.title, book.author, book.year, book.description)
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
async def update_book(book_id: int, book: Book):
    existing_book = db.get_book(book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.update_book(book_id, book.title, book.author, book.year, book.description)
    return {"message": "Book updated successfully"}

# Delete a book
@app.delete("/api/books/{book_id}")
async def delete_book(book_id: int):
    db.delete_book(book_id)
    return {"message": "Book deleted successfully"}
