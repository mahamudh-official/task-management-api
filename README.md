# Task Management API

A production-oriented Task Management REST API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic**, and **JWT-based authentication**.

The project follows a layered architecture with separate **routers, services, repositories, schemas, models, dependencies, exceptions, and exception handlers**.

---

## Features

### Authentication & User Management

* User registration
* User login
* Password hashing with `pwdlib`
* JWT access token authentication
* JWT refresh token authentication
* Refresh token persistence in PostgreSQL
* Refresh token revocation
* Logout using refresh token
* Active/inactive user validation
* Protected API endpoints
* Current-user dependency

### Task Management

* Create tasks
* Get authenticated user's tasks
* Get a single task
* Update tasks
* Delete tasks
* User ownership authorization
* Pagination
* Sorting
* Completion filtering
* Task validation
* Custom task exceptions

### Database

* PostgreSQL
* SQLAlchemy ORM
* Alembic database migrations
* Timezone-aware timestamps
* Refresh token persistence
* Database transaction handling
* Query optimization with composite indexes

### API Architecture

The application follows a layered architecture:

```text
Router
   ↓
Service
   ↓
Repository
   ↓
Database
```

This keeps HTTP handling, business logic, database access, and data models separated.

---

## Tech Stack

| Technology        | Purpose                     |
| ----------------- | --------------------------- |
| Python            | Programming language        |
| FastAPI           | Web framework               |
| PostgreSQL        | Relational database         |
| SQLAlchemy        | ORM                         |
| Alembic           | Database migrations         |
| Pydantic          | Data validation and schemas |
| Pydantic Settings | Environment configuration   |
| PyJWT             | JWT authentication          |
| pwdlib            | Password hashing            |
| Uvicorn           | ASGI server                 |
| Pytest            | Testing framework           |

---

## Project Structure

```text
task-management-api/
│
├── alembic/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│
├── app/
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── logging.py
│   │   └── security.py
│   │
│   ├── dependencies/
│   │   └── auth.py
│   │
│   ├── exception_handlers/
│   │   ├── task.py
│   │   └── user.py
│   │
│   ├── exceptions/
│   │   ├── task.py
│   │   └── user.py
│   │
│   ├── models/
│   │   ├── base.py
│   │   ├── refresh_token.py
│   │   ├── task.py
│   │   └── user.py
│   │
│   ├── repositories/
│   │   ├── refresh_token_repository.py
│   │   ├── task_repository.py
│   │   └── user_repository.py
│   │
│   ├── routers/
│   │   ├── task_routers.py
│   │   └── user_routers.py
│   │
│   ├── schemas/
│   │   ├── task.py
│   │   └── user.py
│   │
│   ├── services/
│   │   ├── task_service.py
│   │   └── user_service.py
│   │
│   └── main.py
│
├── alembic.ini
├── pytest.ini
└── README.md
```

---

# Authentication Flow

The API uses two types of JWT tokens.

### Access Token

The access token is used to access protected endpoints.

```text
Login
  ↓
Access Token
  ↓
Protected API
```

The access token has a relatively short lifetime.

### Refresh Token

The refresh token is used to obtain a new access token when the access token expires.

```text
Login
  ↓
Access Token + Refresh Token
              ↓
        Access Token expires
              ↓
        Refresh Endpoint
              ↓
        New Access Token
```

Refresh tokens are also stored in the database so they can be revoked.

### Logout

Logout revokes the stored refresh token.

```text
Client
  ↓
Refresh Token
  ↓
Logout
  ↓
Refresh Token → revoked
```

A revoked refresh token cannot be used to obtain another access token.

---

# API Endpoints

## Authentication

### Register

```http
POST /auth/register
```

Creates a new user.

### Login

```http
POST /auth/login
```

Authenticates a user and returns:

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```

### Refresh Access Token

```http
POST /auth/refresh
```

Uses a valid refresh token to generate a new access token.

### Logout

```http
POST /auth/logout
```

Revokes the refresh token associated with the session.

---

# Task Endpoints

All task endpoints require authentication.

The client sends the access token using:

```http
Authorization: Bearer <access_token>
```

### Create Task

```http
POST /tasks/
```

Creates a task for the authenticated user.

### Get Tasks

```http
GET /tasks/
```

Supports:

* Pagination
* Limit
* Sorting
* Completion filtering

Example:

```http
GET /tasks/?page=1&limit=10&sort_by=created_at&order=desc
```

Supported sorting fields:

```text
created_at
due_date
```

Supported ordering:

```text
asc
desc
```

Completion filtering:

```http
GET /tasks/?is_completed=true
```

### Get Single Task

```http
GET /tasks/{task_id}
```

Returns a task belonging to the authenticated user.

### Update Task

```http
PATCH /tasks/{task_id}
```

Updates an existing task.

### Delete Task

```http
DELETE /tasks/{task_id}
```

Deletes a task.

---

# Authorization

Task access is restricted by ownership.

A user can only access their own tasks.

The service layer verifies:

```text
task.user_id == current_user.id
```

If another user's task is accessed, the API returns a forbidden response.

This ownership check is applied to:

* Get task
* Update task
* Delete task

---

# Pagination

The task listing API supports pagination.

Example:

```http
GET /tasks/?page=2&limit=10
```

Response contains pagination information including:

```text
items
total
page
limit
total_pages
```

Invalid page numbers are handled through a custom exception.

---

# Database Migrations

Alembic is used to manage database schema changes.

Create a migration:

```bash
alembic revision --autogenerate -m "migration message"
```

Apply migrations:

```bash
alembic upgrade head
```

Check current migration:

```bash
alembic current
```

View migration history:

```bash
alembic history
```

Rollback one migration:

```bash
alembic downgrade -1
```

---

# Database Indexing

Task queries use composite indexes designed around the application's query patterns.

### User + Created At

```text
(user_id, created_at)
```

Index:

```text
ix_tasks_user_created_at
```

### User + Due Date

```text
(user_id, due_date)
```

Index:

```text
ix_tasks_user_due_date
```

These indexes support queries that retrieve a user's tasks while sorting by creation time or due date.

---

# Environment Configuration

Application configuration is loaded from environment variables.

Sensitive values should not be committed to Git.

Typical configuration includes:

```env
APP_NAME=Task Management API

DATABASE_URL=...

SECRET_KEY=...

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRATION_MINUTES=...

REFRESH_TOKEN_EXPIRATION_DAYS=...
```

Use an `.env.example` file to document required environment variables without exposing real secrets.

---

# Local Development

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd task-management-api
```

## 2. Create virtual environment

```bash
python3 -m venv .venv
```

Activate it:

### Linux/macOS

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment

Create your `.env` file and provide the required application and database configuration.

## 5. Run database migrations

```bash
alembic upgrade head
```

## 6. Start the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

These interfaces can be used to inspect and test the available API endpoints.

---

# Error Handling

The project uses custom exceptions for application-level errors.

Examples include:

```text
AuthenticationException
InActiveUserException
UserNotFoundException
UserAlreadyExistsException

TaskNotFoundException
TaskForbiddenException
InvalidTaskPageException
```

Exceptions are handled through dedicated exception handlers.

Typical HTTP responses include:

```text
400 → Bad Request
401 → Authentication failure
403 → Forbidden
404 → Resource not found
409 → Resource conflict
422 → Validation error
```

---

# Transaction Handling

Database write operations use transaction handling through SQLAlchemy.

The general pattern is:

```text
Database operation
      ↓
Commit
      ↓
Success

Error
  ↓
Rollback
  ↓
Exception
```

This helps prevent partially committed database operations.

---

# Security

The application implements several security mechanisms:

* Password hashing
* JWT authentication
* Separate access and refresh tokens
* Refresh token expiration
* Refresh token revocation
* Protected endpoints
* User ownership authorization
* Environment-based secret configuration

Secrets such as database credentials and JWT signing keys should never be committed to source control.

---

# Development Architecture

The project separates responsibilities across multiple layers.

### Router

Handles:

* HTTP requests
* Dependencies
* Request/response models
* Endpoint definitions

### Service

Handles:

* Business logic
* Authentication logic
* Task ownership rules
* Transactions

### Repository

Handles:

* Database queries
* Database persistence
* Entity retrieval

### Model

Represents database tables using SQLAlchemy.

### Schema

Handles request and response validation using Pydantic.

### Dependency

Provides reusable dependencies such as the current authenticated user.

---

# Current Database Models

The application currently contains models for:

```text
User
Task
RefreshToken
```

### User

Stores user account information and authentication-related data.

### Task

Stores:

* Title
* Description
* Due date
* User ownership
* Completion status
* Created timestamp
* Updated timestamp

### RefreshToken

Stores:

* Token
* User ID
* Expiration
* Revocation status
* Creation timestamp

---

# Project Status

Current implementation includes:

* [x] User authentication
* [x] Password hashing
* [x] JWT access tokens
* [x] JWT refresh tokens
* [x] Refresh token persistence
* [x] Refresh token revocation
* [x] Logout
* [x] Current-user authentication dependency
* [x] Task CRUD
* [x] Task ownership authorization
* [x] Pagination
* [x] Sorting
* [x] Completion filtering
* [x] Custom exceptions
* [x] Exception handlers
* [x] PostgreSQL integration
* [x] Alembic migrations
* [x] Database indexes
* [ ] Docker deployment
* [ ] CI/CD
* [ ] Production deployment

---

# Future Improvements

Planned production improvements include:

* Docker containerization
* Docker Compose
* Production database configuration
* CI/CD pipeline
* Cloud deployment
* Automated testing expansion
* Production monitoring
* API performance monitoring
* Production logging improvements

---

# License

This project is currently intended for learning, development, and portfolio purposes.
