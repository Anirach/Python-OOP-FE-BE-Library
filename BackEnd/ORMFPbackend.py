from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional
from pydantic import BaseModel

DATABASE_URL = 'sqlite:///./library.db'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer)
    description = Column(Text)
Base.metadata.create_all(bind=engine)

class BookBase(BaseModel):
    title: str
    author: str
    year: int
    description: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    class Config:
        orm_mode = True
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to get all books from the database
def get_all_books(db: Session):
    return db.query(Book).all()

# Function to add a book to the database
def add_book(db: Session, book: Book):
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

# Function to get a single book by ID from the database
def get_book_by_id(db: Session, book_id: int) -> Optional[Book]:
    return db.query(Book).filter(Book.id == book_id).first()

# Function to update a book by ID in the database
def update_book_by_id(db: Session, book_id: int, updated_data: dict):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        for key, value in updated_data.items():
            setattr(book, key, value)
        db.commit()
        db.refresh(book)
    return book

# Function to delete a book by ID from the database
@app.post("/api/books", response_model=BookResponse)
async def create_book(book: BookCreate, db: Session = next(get_db())):
    db_book = Book(**book.dict())
    new_book = add_book(db, db_book)
    return new_book


@app.get("/api/books/{book_id}", response_model=BookResponse)
async def fetch_single_book(book_id: int, db: Session = next(get_db())):
    book = get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# API Endpoints

# Fetch all books
@app.get("/api/books", response_model=List[Book])
@app.put("/api/books/{book_id}", response_model=BookResponse)
async def modify_book(book_id: int, book: BookCreate, db: Session = next(get_db())):
    return books

# Add a book (backend endpoint)
@app.post("/api/books", response_model=Book)
async def create_book(book: Book, db: Session = next(get_db())):
    new_book = add_book(db, book)
    return new_book

# Fetch a single book
@app.get("/api/books/{book_id}", response_model=Book)
async def fetch_single_book(book_id: int, db: Session = next(get_db())):
    book = get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Update a book
@app.put("/api/books/{book_id}", response_model=Book)
async def modify_book(book_id: int, book: Book, db: Session = next(get_db())):
    existing_book = get_book_by_id(db, book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    updated_book = update_book_by_id(db, book_id, book.dict())
    return updated_book

# Delete a book
@app.delete("/api/books/{book_id}", response_model=dict)
async def remove_book(book_id: int, db: Session = next(get_db())):
    existing_book = get_book_by_id(db, book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    delete_book_by_id(db, book_id)
    return {"message": "Book deleted successfully"}
