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

