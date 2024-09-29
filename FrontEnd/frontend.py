from flask import Flask, render_template, redirect, url_for, request, flash
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key"

BACKEND_URL = "http://127.0.0.1:8000/api"  # FastAPI backend

# Home route to render the book list
@app.route('/')
def index():
    response = requests.get(f"{BACKEND_URL}/books")
    if response.status_code == 200:
        books = response.json()['books']
        return render_template("index.html", books=books)
    return "Error retrieving books", 500

# Route to render the form to add a new book
@app.route('/add', methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        year = int(request.form['year'])
        description = request.form['description']

        response = requests.post(f"{BACKEND_URL}/books", json={"title": title, "author": author, "year": year, "description": description})
        if response.status_code == 200:
            flash("Book added successfully", "success")
            return redirect(url_for('index'))
        else:
            flash("Failed to add book", "danger")

    return render_template("create.html")

# Route to render the book details
@app.route('/books/<int:book_id>')
def book_detail(book_id):
    response = requests.get(f"{BACKEND_URL}/books/{book_id}")
    if response.status_code == 200:
        book = response.json()['book']
        return render_template("book.html", book=book)
    return "Book not found", 404

# Route to render the form to update a book
@app.route('/books/<int:book_id>/edit', methods=["GET", "POST"])
def edit_book(book_id):
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        year = int(request.form['year'])
        description = request.form['description']

        response = requests.put(f"{BACKEND_URL}/books/{book_id}", json={"title": title, "author": author, "year": year, "description": description})
        if response.status_code == 200:
            flash("Book updated successfully", "success")
            return redirect(url_for('index'))
        else:
            flash("Failed to update book", "danger")

    # Fetch book details for the form
    response = requests.get(f"{BACKEND_URL}/books/{book_id}")
    if response.status_code == 200:
        book = response.json()['book']
        return render_template("edit.html", book=book)
    return "Book not found", 404

# Delete a book
@app.route('/books/<int:book_id>/delete', methods=["GET", "POST"])
def delete_book(book_id):
    print("delete_book")
    response = requests.delete(f"{BACKEND_URL}/books/{book_id}")
    if response.status_code == 200:
        flash("Book deleted successfully", "success")
    else:
        flash("Failed to delete book", "danger")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
