FastAPI Projects Collection

This repository contains four FastAPI projects demonstrating secure APIs, role-based access, and token-based authentication.

Project 1: Secure Student Portal API
Goal: Build an API where students can register, log in, and view their grades securely.
Features: Student class with username, hashed password, grades list. Endpoints: POST /register/ to register students, POST /login/ to authenticate and return a token, GET /grades/ to view grades (requires authentication). Data stored in students.json. Error handling using try-except.
How to run:

pip install fastapi uvicorn passlib[bcrypt]
uvicorn main:app --reload


Swagger UI: http://127.0.0.1:8000/docs

Project 2: Role-Based Shopping API
Goal: Create an API where admins can add products and all users can browse and shop.
Features: User class with roles (admin or customer). Module auth.py handles authentication and role-based access. Endpoints: POST /admin/add_product/ (admin only), GET /products/ (public), POST /cart/add/ (authenticated users only). Data stored in products.json and cart.json. Dependency injection used for role checking.
How to run:

pip install fastapi uvicorn passlib[bcrypt]
uvicorn main:app --reload


Usage: Register admin and customer users, login and use token for authentication, admin adds products, customers add to cart and view cart.

Project 3: Job Application Tracker
Goal: Track job applications where each user can only see their own applications.
Features: JobApplication class with job title, company, date applied, status. Endpoints: POST /applications/ to add a job application, GET /applications/ to view your own applications. Data stored in applications.json. Dependency injection used to filter results per logged-in user.
How to run:

pip install fastapi uvicorn passlib[bcrypt]
uvicorn main:app --reload


Usage: Register and login, add applications, view applications (each user only sees their own).

Project 4: Notes API with JWT Authentication
Goal: Secure notes management API using JWT tokens.
Features: Note class with title, content, date. Endpoints: POST /login/ to return JWT token, POST /notes/ to add a note (requires token), GET /notes/ to view your notes. Data stored in notes.json per user. JWT authentication and secure routes implemented.
How to run:

pip install fastapi uvicorn passlib[bcrypt] python-jose[cryptography]
uvicorn main:app --reload


Usage: Register a user, login to get JWT token, authorize in Swagger with Bearer <token>, add and view notes.

General Notes: All projects use FastAPI, UVicorn, and Passlib for password hashing. JSON files are used for persistent storage per project. Swagger UI provides an easy interface to test all endpoints: http://127.0.0.1:8000/docs