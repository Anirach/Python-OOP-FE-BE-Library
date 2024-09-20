from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import Book
from database import Database

app = FastAPI()
templates = Jinja2Templates(directory="templates")
db = Database()

# Home route to render the book list
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    books = db.get_books()
    return templates.TemplateResponse("index.html", {"request": request, "books": books})

# Add a book (backend endpoint)
@app.post("/add")
async def add_book(title: str = Form(...), author: str = Form(...), year: int = Form(...), description: str = Form(...)):
    db.add_book(title, author, year, description)
    return {"message": "Book added successfully"}

# Fetch a single book
@app.get("/books/{book_id}", response_class=HTMLResponse)
async def get_book(book_id: int, request: Request):
    book = db.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse("book.html", {"request": request, "book": book})

# Delete a book
@app.post("/books/{book_id}/delete")
async def delete_book(book_id: int):
    db.delete_book(book_id)
    return {"message": "Book deleted successfully"}

# Close the database connection when the app shuts down
@app.on_event("shutdown")
def shutdown():
    db.close()
