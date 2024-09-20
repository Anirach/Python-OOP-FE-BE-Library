from pydantic import BaseModel

# Pydantic model for the Book
class Book(BaseModel):
    title: str
    author: str
    year: int
    description: str
