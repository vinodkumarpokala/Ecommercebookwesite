
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
