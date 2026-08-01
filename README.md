# Expense Tracker API

A Django REST Framework expense tracker API with JWT authentication, user-owned categories and expenses, filtering, search, ordering, pagination, analytics endpoints, Swagger/ReDoc documentation, and Docker-based deployment with Nginx, Gunicorn, and PostgreSQL.

![Python](https://img.shields.io/badge/Python-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-ff1709?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?logo=nginx&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?logo=gunicorn&logoColor=white)

## Project Overview

This repository demonstrates a production-style backend built with Django REST Framework, JWT authentication, PostgreSQL, Docker, Docker Compose, Gunicorn, and Nginx. It is structured so each authenticated user can manage only their own categories and expenses.

## Why this project?

This project was built to practice designing a production-style Django REST Framework backend. It focuses on JWT authentication, user-specific ownership rules, PostgreSQL persistence, and containerized deployment with Docker, Gunicorn, and Nginx.

It serves as a compact example of a REST API that can run locally or behind a production-style Docker stack.

## Features

- Authentication
  - Email-based custom user model
  - JWT authentication with access and refresh tokens
  - Register and fetch the current authenticated user
- Category Management
  - CRUD for categories
  - Category names normalized before save
- Expense Management
  - CRUD for expenses
  - Expense validation for amount, title, and category ownership
- Ownership & Permissions
  - User-specific ownership and object-level access control
- Filtering
  - Filtering by category, date, and amount ranges
- Search
  - Search across expense title and notes
- Ordering
  - Ordering by amount, expense date, and creation time
- Pagination
  - Paginated expense listing with client-controlled page size
- Analytics
  - Analytics endpoints for monthly and category-based summaries
- API Documentation
  - Swagger UI and ReDoc documentation
- Docker Deployment
  - Dockerized deployment with Nginx, Gunicorn, and PostgreSQL

## Architecture Overview

```text
Client (Browser/Postman)
    ↓
  Nginx (Reverse Proxy)
    ↓
  Gunicorn (WSGI Application Server)
    ↓
  Django REST Framework
    ↓
  PostgreSQL
```

- Nginx listens on port 80, serves `/static/`, and proxies application requests to the web container.
- Gunicorn runs inside the `web` container and serves the Django WSGI application.
- Django REST Framework exposes the API, handles authentication, validation, filtering, and analytics.
- PostgreSQL stores users, categories, expenses, and related metadata.

## Tech Stack

### Language

- Python

### Framework

- Django
- Django REST Framework
- django-filter

### Database

- PostgreSQL

### Authentication

- Simple JWT

### API Documentation

- drf-spectacular
- Swagger UI
- ReDoc

### Deployment

- Docker
- Docker Compose
- Gunicorn
- Nginx

### Configuration

- python-decouple

## Project Structure

```text
.
├── core/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── expenses/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── filters.py
│   ├── permissions.py
│   ├── pagination.py
│   └── admin.py
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── requirements.txt
├── README.md
├── .env                  # create manually
└── staticfiles/
```

## Prerequisites

### Required

- Git
- Docker Desktop

### Optional (Local Development)

- Python 3.12+
- PostgreSQL

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd Expense-Tracker-API
```

### 2. Create a `.env` file in the project root

The repository ignores `.env`, so create it manually.

```env
SECRET_KEY=your-secret-key
DEBUG=False

ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=expense_tracker_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=db
DB_PORT=5432
```

Notes:

- `ALLOWED_HOSTS` is a comma-separated list.
- Docker: `DB_HOST=db`
- Local Development: `DB_HOST=localhost`

## Option 1 — Run with Docker (Recommended)

This is the primary setup method.

### 1. Build and start the containers

This command builds the images if needed and starts all services in detached mode.

```bash
docker compose up --build -d
```

### 2. Apply migrations

```bash
docker compose exec web python manage.py migrate
```

### 3. Collect static files

```bash
docker compose exec web python manage.py collectstatic
```

This copies static assets into the shared Docker volume so Nginx can serve them directly.

### 4. Create a superuser

```bash
docker compose exec web python manage.py createsuperuser
```

## Option 2 — Run Locally (Development)

Use this workflow if you want to run Django directly on your machine.

### 1. Optional: create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure PostgreSQL locally

Use a local PostgreSQL instance and set `DB_HOST` to your local database host, such as `localhost`.

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

## Verify the Setup

Use these checks after starting the project:

- `docker compose ps` to confirm the containers are running
- Django Admin: [http://localhost/admin/](http://localhost/admin/)
- Swagger UI: [http://localhost/api/docs/](http://localhost/api/docs/)
- ReDoc: [http://localhost/api/redoc/](http://localhost/api/redoc/)

## Application URLs

The following application URLs are accessible from `http://localhost` during local development:

| URL | Description |
| --- | --- |
| `http://localhost/admin/` | Django admin |
| `http://localhost/api/users/register/` | Register a new user |
| `http://localhost/api/users/me/` | Current authenticated user |
| `http://localhost/api/login/` | Obtain JWT tokens |
| `http://localhost/api/login/refresh/` | Refresh JWT access token |
| `http://localhost/api/categories/` | Category API |
| `http://localhost/api/expenses/` | Expense API |
| `http://localhost/api/expenses/monthly-summary/` | Monthly analytics |
| `http://localhost/api/expenses/category-summary/` | Category analytics |
| `http://localhost/api/expenses/top-spending-categories/` | Top spending categories |
| `http://localhost/api/docs/` | Swagger UI |
| `http://localhost/api/redoc/` | ReDoc |
| `http://localhost/api/schema/` | OpenAPI schema |

## Docker Setup

The application is composed of three Docker services:

- `nginx`: reverse proxy and static file server
- `web`: Django application running under Gunicorn
- `db`: PostgreSQL database

The `web` container reads environment variables from `.env`, and Nginx serves static assets from the shared `staticfiles` volume after `collectstatic` copies them there.

## Environment Variables

The project reads the following variables through `python-decouple` and Docker Compose:

- `SECRET_KEY`: Django secret key
- `DEBUG`: boolean debug flag
- `ALLOWED_HOSTS`: comma-separated list of allowed hostnames
- `DB_NAME`: PostgreSQL database name
- `DB_USER`: PostgreSQL username
- `DB_PASSWORD`: PostgreSQL password
- `DB_HOST`: database host, typically `db` in Docker
- `DB_PORT`: database port, typically `5432`

## Authentication

Authentication is handled with JWT through Simple JWT.

### Register

```http
POST /api/users/register/
```

Example body:

```json
{
  "email": "user@example.com",
  "username": "user",
  "password": "yourpassword"
}
```

### Login

```http
POST /api/login/
```

Example body:

```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

### Refresh access token

```http
POST /api/login/refresh/
```

### Current user

```http
GET /api/users/me/
Authorization: Bearer <access-token>
```

Protected endpoints require the access token in the `Authorization` header.

## API Endpoints

All authenticated endpoints require `Authorization: Bearer <access-token>`.

### Authentication and user

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/api/users/register/` | Register a new user |
| POST | `/api/login/` | Obtain access and refresh tokens |
| POST | `/api/login/refresh/` | Refresh an access token |
| GET | `/api/users/me/` | Return the authenticated user |

### Categories

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/categories/` | List the current user’s categories |
| POST | `/api/categories/` | Create a category |
| GET | `/api/categories/{id}/` | Retrieve a category |
| PUT | `/api/categories/{id}/` | Replace a category |
| PATCH | `/api/categories/{id}/` | Partially update a category |
| DELETE | `/api/categories/{id}/` | Delete a category |

Categories are user-owned and names are normalized before saving. Duplicate category names per user are prevented.

### Expenses

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/expenses/` | List the current user’s expenses |
| POST | `/api/expenses/` | Create an expense |
| GET | `/api/expenses/{id}/` | Retrieve an expense |
| PUT | `/api/expenses/{id}/` | Replace an expense |
| PATCH | `/api/expenses/{id}/` | Partially update an expense |
| DELETE | `/api/expenses/{id}/` | Delete an expense |

Expense payload example:

```json
{
  "title": "Lunch",
  "amount": "150.00",
  "expense_date": "2026-06-27",
  "category": 1,
  "notes": "Biryani"
}
```

## Filtering, Search, Ordering

The expense list endpoint supports the following query parameters:

### Filtering

```http
GET /api/expenses/?category=1
GET /api/expenses/?expense_date=2026-06-27
GET /api/expenses/?min_amount=100&max_amount=500
GET /api/expenses/?expense_date_after=2026-06-01&expense_date_before=2026-06-30
```

### Search

```http
GET /api/expenses/?search=lunch
```

Searches across `title` and `notes`.

### Ordering

```http
GET /api/expenses/?ordering=amount
GET /api/expenses/?ordering=-amount
GET /api/expenses/?ordering=expense_date
GET /api/expenses/?ordering=-created_at
```

You can combine these parameters in a single request.

## Pagination

Expense lists are paginated with page-number pagination.

- Default page size: `10`
- Maximum page size: `100`
- Query parameters: `page`, `page_size`

Example:

```http
GET /api/expenses/?page=2&page_size=20
```

Typical response shape:

```json
{
  "count": 47,
  "next": "http://localhost/api/expenses/?page=3",
  "previous": "http://localhost/api/expenses/?page=1",
  "results": []
}
```

## Analytics Endpoints

### Monthly summary

```http
GET /api/expenses/monthly-summary/
```

Groups expenses by month and returns total amount plus count.

### Category summary

```http
GET /api/expenses/category-summary/
```

Returns totals, counts, and averages per category.

### Top spending categories

```http
GET /api/expenses/top-spending-categories/
GET /api/expenses/top-spending-categories/?limit=3
```

Returns the highest-spending categories for the authenticated user. The default limit is `5`.

## API Documentation

The API schema and interactive docs are automatically generated with drf-spectacular.

The API schema and interactive docs are available at:

- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`
- OpenAPI schema: `/api/schema/`

## Django Admin

The Django admin is available at `/admin/` for managing users, categories, and expenses.

## Useful Docker Commands

```bash
docker compose up -d
docker compose up --build -d
docker compose logs -f
docker compose stop
docker compose down
docker compose restart
docker compose ps
```

## Production Architecture

In production, requests flow through Nginx first. Nginx terminates external HTTP traffic, serves static files from the shared volume, and forwards application requests to Gunicorn. Gunicorn runs the Django application code, which handles authentication, validation, filtering, and analytics before reading or writing data in PostgreSQL.

- Nginx: reverse proxy
- Gunicorn: WSGI application server for Django
- Django: API, authentication, validation, filtering, and analytics
- PostgreSQL: persistent storage for users, categories, and expenses

## Future Improvements

- Add automated tests for serializers, permissions, filters, and analytics endpoints
- Add CI checks for linting, migrations, and test execution
- Add Docker health checks and restart policies
- Add HTTPS termination and production hardening for Nginx
- Add export/reporting features for expense data
