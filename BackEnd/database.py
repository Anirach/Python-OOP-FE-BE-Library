import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('library.db')
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        # Create the books table if it does not exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS books
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT, author TEXT, year INTEGER, description TEXT)''')
        self.connection.commit()

    def add_book(self, title, author, year, description):
        self.cursor.execute("INSERT INTO books (title, author, year, description) VALUES (?, ?, ?, ?)",
                            (title, author, year, description))
        self.connection.commit()

    def get_books(self):
        self.cursor.execute("SELECT * FROM books")
        return self.cursor.fetchall()

    def get_book(self, book_id):
        self.cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
        return self.cursor.fetchone()

    def delete_book(self, book_id):
        self.cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        self.connection.commit()

    def update_book(self, book_id: int, title: str, author: str, year: int, description: str):
        self.cursor.execute('''UPDATE books
                               SET title = ?, author = ?, year = ?, description = ?
                               WHERE id = ?''', (title, author, year, description, book_id))
        self.connection.commit()
        print(f'Book with id {book_id} updated successfully')


    def close(self):
        self.connection.close()
