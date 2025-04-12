# Ecommercebookwesite
sample website for testing


Okay, let's outline a basic full-stack web application using Python for the frontend (with a lightweight framework), backend (with Flask), and database (with SQLite).
I. Database (SQLite)
SQLite is a file-based database, so you don't need a separate server running. We'll define a table for storing book information.
# backend/database.py

import sqlite3

DATABASE_FILE = 'books.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            cover_image TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print(f"Database '{DATABASE_FILE}' initialized.")

II. Backend (Flask)
Create a folder structure for your backend (e.g., backend). Inside it, you'll have files like app.py and database.py (as above).
1. backend/app.py (Flask application):
from flask import Flask, request, jsonify
from flask_cors import CORS
import database

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

@app.route('/api/books', methods=['GET'])
def get_books():
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return jsonify([dict(book) for book in books])

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
    book = cursor.fetchone()
    conn.close()
    if book:
        return jsonify(dict(book))
    return jsonify({'message': 'Book not found'}), 404

@app.route('/api/books', methods=['POST'])
def create_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    price = data.get('price')
    description = data.get('description')
    cover_image = data.get('cover_image')

    if not all([title, author, isbn, price]):
        return jsonify({'message': 'Missing required fields'}), 400

    conn = database.get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO books (title, author, isbn, price, description, cover_image)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, author, isbn, price, description, cover_image))
        conn.commit()
        book_id = cursor.lastrowid
        conn.close()
        return jsonify({'id': book_id, 'message': 'Book created successfully'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'message': 'ISBN already exists'}), 409

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    price = data.get('price')
    description = data.get('description')
    cover_image = data.get('cover_image')

    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
    existing_book = cursor.fetchone()

    if not existing_book:
        conn.close()
        return jsonify({'message': 'Book not found'}), 404

    update_fields = {}
    if title is not None:
        update_fields['title'] = title
    if author is not None:
        update_fields['author'] = author
    if isbn is not None:
        update_fields['isbn'] = isbn
    if price is not None:
        update_fields['price'] = price
    if description is not None:
        update_fields['description'] = description
    if cover_image is not None:
        update_fields['cover_image'] = cover_image

    if not update_fields:
        conn.close()
        return jsonify({'message': 'No fields to update'}), 200

    set_clause = ', '.join(f"{key}=?" for key in update_fields)
    values = list(update_fields.values())
    values.append(book_id)

    try:
        cursor.execute(f"UPDATE books SET {set_clause} WHERE id=?", tuple(values))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Book updated successfully'}), 200
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'message': 'ISBN already exists'}), 409

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book deleted successfully'}), 200

if __name__ == '__main__':
    database.init_db()
    app.run(debug=True)

To run the backend:
 * Create a folder named backend.
 * Save the database.py and app.py files inside the backend folder.
 * Open your terminal, navigate to the backend folder.
 * Install Flask and Flask-CORS: pip install Flask Flask-CORS
 * Run the Flask application: python app.py
   The server will typically start on http://127.0.0.1:5000/.
III. Frontend (Basic HTML, CSS, and JavaScript)
For a simple Python-only full-stack example, we can use basic HTML, CSS, and JavaScript to interact with the Flask backend. Create a folder named frontend in the same directory as your backend folder.
1. frontend/index.html:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bookstore</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Bookstore</h1>

    <div id="book-list">
        </div>

    <h2>Add New Book</h2>
    <form id="add-book-form">
        <div>
            <label for="title">Title:</label>
            <input type="text" id="title" name="title" required>
        </div>
        <div>
            <label for="author">Author:</label>
            <input type="text" id="author" name="author" required>
        </div>
        <div>
            <label for="isbn">ISBN:</label>
            <input type="text" id="isbn" name="isbn" required>
        </div>
        <div>
            <label for="price">Price:</label>
            <input type="number" id="price" name="price" required>
        </div>
        <div>
            <label for="description">Description:</label>
            <textarea id="description" name="description"></textarea>
        </div>
        <div>
            <label for="cover_image">Cover Image URL:</label>
            <input type="text" id="cover_image" name="cover_image">
        </div>
        <button type="submit">Add Book</button>
    </form>

    <h2>Edit Book</h2>
    <form id="edit-book-form">
        <input type="hidden" id="edit-id" name="id">
        <div>
            <label for="edit-title">Title:</label>
            <input type="text" id="edit-title" name="title" required>
        </div>
        <div>
            <label for="edit-author">Author:</label>
            <input type="text" id="edit-author" name="author" required>
        </div>
        <div>
            <label for="edit-isbn">ISBN:</label>
            <input type="text" id="edit-isbn" name="isbn" required>
        </div>
        <div>
            <label for="edit-price">Price:</label>
            <input type="number" id="edit-price" name="price" required>
        </div>
        <div>
            <label for="edit-description">Description:</label>
            <textarea id="edit-description" name="description"></textarea>
        </div>
        <div>
            <label for="edit-cover_image">Cover Image URL:</label>
            <input type="text" id="edit-cover_image" name="cover_image">
        </div>
        <button type="submit">Update Book</button>
    </form>

    <script src="script.js"></script>
</body>
</html>

2. frontend/style.css:
body {
    font-family: sans-serif;
    margin: 20px;
}

#book-list {
    margin-bottom: 20px;
    border: 1px solid #ccc;
    padding: 10px;
}

.book-item {
    border-bottom: 1px solid #eee;
    padding: 8px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.book-item span {
    flex-grow: 1;
    margin-right: 10px;
}

.book-item button {
    margin-left: 5px;
}

#add-book-form, #edit-book-form {
    margin-top: 20px;
    padding: 15px;
    border: 1px solid #ccc;
}

#add-book-form div, #edit-book-form div {
    margin-bottom: 10px;
}

3. frontend/script.js:
const bookListDiv = document.getElementById('book-list');
const addBookForm = document.getElementById('add-book-form');
const editBookForm = document.getElementById('edit-book-form');
const editIdInput = document.getElementById('edit-id');
const editTitleInput = document.getElementById('edit-title');
const editAuthorInput = document.getElementById('edit-author');
const editIsbnInput = document.getElementById('edit-isbn');
const editPriceInput = document.getElementById('edit-price');
const editDescriptionInput = document.getElementById('edit-description');
const editCoverImageInput = document.getElementById('edit-cover_image');

async function fetchBooks() {
    const response = await fetch('http://localhost:5000/api/books');
    const books = await response.json();
    displayBooks(books);
}

function displayBooks(books) {
    bookListDiv.innerHTML = '';
    books.forEach(book => {
        const bookItem = document.createElement('div');
        bookItem.classList.add('book-item');
        bookItem.innerHTML = `
            <span>${book.title} by ${book.author} ($${book.price})</span>
            <button onclick="editBook('${book.id}', '${book.title}', '${book.author}', '${book.isbn}', '${book.price}', '${book.description || ''}', '${book.cover_image || ''}')">Edit</button>
            <button onclick="deleteBook('${book.id}')">Delete</button>
        `;
        bookListDiv.appendChild(bookItem);
    });
}

addBookForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(addBookForm);
    const bookData = Object.fromEntries(formData.entries());

    const response = await fetch('http://localhost:5000/api/books', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookData),
    });

    if (response.ok) {
        fetchBooks();
        addBookForm.reset();
    } else {
        const error = await response.json();
        alert(`Error adding book: ${error.message}`);
    }
});

async function editBook(id, title, author, isbn, price, description, cover_image) {
    editIdInput.value = id;
    editTitleInput.value = title;
    editAuthorInput.value = author;
    editIsbnInput.value = isbn;
    editPriceInput.value = price;
    editDescriptionInput.value = description;
    editCoverImageInput.value = cover_image;
}

editBookForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(editBookForm);
    const bookData = Object.fromEntries(formData.entries());
    const id = bookData.id;
    delete bookData.id; // Don't send ID in the update body

    const response = await fetch(`http://localhost:5000/api/books/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookData),
    });

    if (response.ok) {
        fetchBooks();
        editBookForm.reset();
    } else {
        const error = await response.json();
        alert(`Error updating book: ${error.message}`);
    }
});

async function deleteBook(id) {
    if (confirm('Are you sure you want to delete this book?')) {
        const response = await fetch(`http://localhost:5000/api/books/${id}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            fetchBooks();
        } else {
            const error = await response.json();
            alert(`Error deleting book: ${error.message}`);
        }
    }
}

// Initial fetch of books when the page loads
fetchBooks();

To run the frontend:
 * Create a folder named frontend in the same directory as your backend folder.
 * Save index.html, style.css, and script.js inside the frontend folder.
 * Open the frontend/index.html file in your web browser.
How it works:
 * Database (SQLite): The database.py script initializes and interacts with the books.db file.
 * Backend (Flask): The app.py script creates a Flask API with endpoints for:
   * GET /api/books: Fetching all books.
   * GET /api/books/<id>: Fetching a specific book.
   * POST /api/books: Creating a new book.
   * PUT /api/books/<id>: Updating an existing book.
   * DELETE /api/books/<id>: Deleting a book.
   * flask-cors is used to allow requests from the frontend (which runs on a different origin by default).
 * Frontend (HTML, CSS, JavaScript):
   * index.html: Provides the basic structure and forms for displaying, adding, and editing books.
   * style.css: Adds basic styling to the page.
   * script.js: Handles the dynamic behavior:
     * Fetches books from the Flask API on page load.
     * Displays the fetched books.
     * Handles form submissions for adding and updating books, sending data to the Flask API.
     * Handles deleting books via the Flask API.
This provides a basic full-stack application in Python. For more complex frontends, you would typically use a dedicated JavaScript framework like React, Angular, or Vue.js.
