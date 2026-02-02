# FastAPI Task Manager

A simple **CRUD Task Management API** built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy (async)**. The project supports user authentication with **JWT tokens**, password hashing with **Argon2**, and is fully containerized using **Docker** and **Docker Compose**.

---

## Features

- User registration and login with JWT authentication
- Password hashing using Argon2
- Role-based user management (first user is `admin`, others are `user`)
- Async CRUD operations for tasks:
  - Create task
  - Fetch all tasks
  - Fetch task by ID
  - Update task
  - Delete task
- Fully containerized with Docker and Docker Compose
- Auto-generated database migrations using Alembic
- Interactive API documentation via **Swagger UI**

---

## Tech Stack

- **Backend:** FastAPI
- **Database:** PostgreSQL (asyncpg)
- **ORM:** SQLAlchemy (Async)
- **Migrations:** Alembic
- **Auth:** JWT, OAuth2 PasswordBearer
- **Password Hashing:** PassLib Argon2
- **Containerization:** Docker, Docker Compose

---

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.9.12+ (if running locally without Docker)

### Environment Variables

Create a `.env` file with the following variables:
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=task_notes_db
SECRET=your_jwt_secret
JWT_ALGORITHM=HS256

## Running Instructions

### 1. Clone the repository


* git clone https://github.com/S2442001/task-management-api-fastapi
* cd FastAPI Task & Notes Manager

### 2. Running with Docker

* Build & Start Container: docker-compose up --build
* Backend API will be available at: http://localhost:8000
* Run Alembic migrations inside container: alembic upgrade head

### 3. Running Locally (Without Docker)

* Create a virtual environment and activate it: 
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
---
* Install dependencies: pip install -r requirements.txt
* Apply Alembic migrations: alembic upgrade head
* Start FastAPI server: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
* Access the API: http://localhost:8000
* Swagger UI for testing endpoints: http://localhost:8000/docs
---
### Notes

* JWT access tokens expire after 30 minutes. Re-login if token expires.
* First registered user becomes admin, others become user.
* Use Swagger UI to interact with endpoints; no separate frontend is required.
* Docker ensures a fully isolated environment for app and PostgreSQL database.
---
### API Screenshots
<img width="1828" height="971" alt="image" src="https://github.com/user-attachments/assets/98f1d429-c341-42e2-b200-89f2f66d2d02" />


