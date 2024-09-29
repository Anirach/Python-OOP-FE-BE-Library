from fastapi import FastAPI, HTTPException
from models import Book
from typing import List, Optional
from contextlib import asynccontextmanager
import sqlite3
from contextlib import contextmanager

DATABASE = '/Users/anirachmingkhwan/Code/PythonLibraryProject/BackEnd/library.db'

app = FastAPI()

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL,
            description TEXT
        )
        ''')
        conn.commit()

init_db()

@asynccontextmanager
async def lifespan():
    yield

# Function to get all books from the database
def get_all_books():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
        return [{"id": row[0], "title": row[1], "author": row[2], "year": row[3], "description": row[4]} for row in books]

# Function to add a book to the database
def add_book(book: dict):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO books (title, author, year, description)
        VALUES (?, ?, ?, ?)
        ''', (book["title"], book["author"], book["year"], book["description"]))
        conn.commit()

# Function to get a single book by ID from the database
def get_book_by_id(book_id: int) -> Optional[dict]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        row = cursor.fetchone()
        if row:
            return {"id": row[0], "title": row[1], "author": row[2], "year": row[3], "description": row[4]}
        return None

# Function to update a book by ID in the database
def update_book_by_id(book_id: int, updated_data: dict):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE books
        SET title = ?, author = ?, year = ?, description = ?
        WHERE id = ?
        ''', (updated_data["title"], updated_data["author"], updated_data["year"], updated_data["description"], book_id))
        conn.commit()

# Function to delete a book by ID from the database
def delete_book_by_id(book_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()

# API Endpoints

# Fetch all books
@app.get("/api/books")
async def fetch_books():
    books = get_all_books()
    return {"books": books}

# Add a book (backend endpoint)
@app.post("/api/books")
async def create_book(book: Book):
    new_book = {
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "description": book.description,
    }
    add_book(new_book)
    return {"message": "Book added successfully"}

# Fetch a single book
@app.get("/api/books/{book_id}")
async def fetch_single_book(book_id: int):
    book = get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"book": book}

# Update a book
@app.put("/api/books/{book_id}")
async def modify_book(book_id: int, book: Book):
    existing_book = get_book_by_id(book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    updated_book = {
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "description": book.description,
    }
    update_book_by_id(book_id, updated_book)
    return {"message": "Book updated successfully"}

# Delete a book
@app.delete("/api/books/{book_id}")
async def remove_book(book_id: int):
    existing_book = get_book_by_id(book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    delete_book_by_id(book_id)
    return {"message": "Book deleted successfully"}
