# Library Management System 📚
A robust backend implementation for a Library Management System built using Python Django and MySQL. This project implements a fully functional backend based on provided frontend templates, 
handling user authentication, book inventory management, and borrowing workflows.

## Features
### 1. User Authentication
- Secure Login/Logout functionality.
- Session management to persist user states.
- Access control decorators (preventing unauthorized access to restricted actions).

### 2. Book Management (CRUD)
- View: Browse the complete library catalog.
- Search: Filter books by Title or Author.
- Add: Administrators can add new books to the inventory.
- Edit: Update details of existing books.
- Delete: Remove books from the system.

### 3. Circulation System (Borrowing)
- Borrow: Check out available books (auto-decrements stock).
- Return: Return books (auto-increments stock).
- History: Track current and past borrowed books with due dates.
- Validation: Prevents borrowing if stock is 0.

## Technology Stack
- Backend Framework: Django 4.x / 5.x
- Database: MySQL
- Frontend: HTML, CSS (Bootstrap)
