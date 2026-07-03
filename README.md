# Expense Tracker API

A production-oriented REST API for tracking personal expenses built with Django and Django REST Framework. Supports JWT authentication, category and expense management, filtering, search, ordering, pagination, and analytics endpoints.

The project is designed to reflect real backend development practices — ownership-based access control, clean API design, query optimization, and auto-generated API documentation.

---

## Features

- User registration and login with JWT access and refresh tokens
- Custom user model with email-based authentication
- Create, edit, and delete expense categories (per user, case-insensitive)
- Full CRUD for expenses with category association
- Ownership enforcement — users can only access their own data
- Custom permission class for object-level access control
- Filtering by category, date range, and amount range
- Search expenses by title and notes
- Ordering by amount, date, or creation time
- Paginated responses with client-controlled page size
- Analytics endpoints — monthly summary, category-wise spending, top spending categories
- Auto-generated API documentation with Swagger UI and ReDoc

---

## Tech Stack

- Python 3.x
- Django
- Django REST Framework
- Simple JWT
- django-filter
- drf-spectacular
- SQLite

---

## Project Structure

```
expense-tracker-api/
│
├── core/                  # Django project configuration
├── users/                 # Custom user model, registration, auth APIs
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── expenses/              # Categories, expenses, filters, permissions, analytics
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── filters.py
│   ├── permissions.py
│   ├── pagination.py
│   └── admin.py
├── manage.py
├── requirements.txt
└── .env
```

---

## Getting Started

### Prerequisites

- Python installed on your machine
- `pip` available for installing dependencies

### Installation

1. Clone the repository.

2. Create and activate a virtual environment.

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

3. Install the dependencies.

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory.

```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

5. Apply database migrations.

```bash
python manage.py migrate
```

6. Create a superuser to access the Django admin.

```bash
python manage.py createsuperuser
```

7. Start the development server.

```bash
python manage.py runserver
```

---

## Authentication

This API uses JWT (JSON Web Tokens) via Simple JWT.

### Register

```
POST /api/users/register/
```

```json
{
    "email": "user@example.com",
    "username": "user",
    "password": "yourpassword"
}
```

### Login

```
POST /api/login/
```

```json
{
    "email": "user@example.com",
    "password": "yourpassword"
}
```

Response:

```json
{
    "access": "your-access-token",
    "refresh": "your-refresh-token"
}
```

### Refresh Token

```
POST /api/login/refresh/
```

### Current User

```
GET /api/users/me/
Authorization: Bearer your-access-token
```

---

## API Endpoints

All endpoints require `Authorization: Bearer <access-token>` unless stated otherwise.

### Categories

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/categories/` | List all your categories |
| POST | `/api/categories/` | Create a new category |
| GET | `/api/categories/<id>/` | Retrieve a category |
| PUT/PATCH | `/api/categories/<id>/` | Update a category |
| DELETE | `/api/categories/<id>/` | Delete a category |

> Deleting a category will fail if any expenses are linked to it.

### Expenses

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/expenses/` | List all your expenses |
| POST | `/api/expenses/` | Create a new expense |
| GET | `/api/expenses/<id>/` | Retrieve an expense |
| PUT/PATCH | `/api/expenses/<id>/` | Update an expense |
| DELETE | `/api/expenses/<id>/` | Delete an expense |

### Example Request Body (Create Expense)

```json
{
    "title": "Lunch",
    "amount": "150.00",
    "expense_date": "2026-06-27",
    "category": 1,
    "notes": "Biryani"
}
```

### Example Response

```json
{
    "id": 1,
    "title": "Lunch",
    "amount": "150.00",
    "expense_date": "2026-06-27",
    "notes": "Biryani",
    "category": 1,
    "category_detail": {
        "id": 1,
        "name": "Food"
    },
    "created_at": "2026-06-27T10:00:00Z",
    "updated_at": "2026-06-27T10:00:00Z"
}
```

---

## Filtering, Search, and Ordering

### Filtering

```
GET /api/expenses/?category=1
GET /api/expenses/?min_amount=100&max_amount=500
GET /api/expenses/?expense_date=2026-06-27
GET /api/expenses/?expense_date_after=2026-06-01&expense_date_before=2026-06-30
```

### Search

```
GET /api/expenses/?search=lunch
```

Searches across `title` and `notes`.

### Ordering

```
GET /api/expenses/?ordering=amount         # ascending
GET /api/expenses/?ordering=-amount        # descending
GET /api/expenses/?ordering=expense_date
GET /api/expenses/?ordering=-created_at
```

### Combine Everything

```
GET /api/expenses/?category=1&search=lunch&ordering=-amount&page=2&page_size=5
```

---

## Pagination

Responses are paginated. Default page size is 10.

```
GET /api/expenses/?page=2
GET /api/expenses/?page_size=20       # client-controlled, max 100
```

Response shape:

```json
{
    "count": 47,
    "next": "http://localhost:8000/api/expenses/?page=2",
    "previous": null,
    "results": [...]
}
```

---

## Analytics Endpoints

### Monthly Summary

```
GET /api/expenses/monthly-summary/
```

Returns total amount and expense count grouped by month.

```json
[
    {"month": "2026-06-01", "total": "4500.00", "count": 12},
    {"month": "2026-05-01", "total": "3200.00", "count": 9}
]
```

### Category Summary

```
GET /api/expenses/category-summary/
```

Returns total, count, and average spending per category.

```json
[
    {"category__id": 1, "category__name": "Food", "total": "1200.00", "count": 8, "average": "150.00"},
    {"category__id": 2, "category__name": "Travel", "total": "800.00", "count": 3, "average": "266.67"}
]
```

### Top Spending Categories

```
GET /api/expenses/top-spending-categories/
GET /api/expenses/top-spending-categories/?limit=3
```

Returns top N categories by total spending. Defaults to 5.

---

## API Documentation

Start the server and visit:

- **Swagger UI** — `http://localhost:8000/api/docs/`
- **ReDoc** — `http://localhost:8000/api/redoc/`

To export the schema as a file:

```bash
python manage.py spectacular --color --file schema.yml
```

---

## Admin

The Django admin is available at `/admin/` for managing users, categories, and expenses.

---

## Development Notes

- The project uses SQLite by default, making it easy to run locally with no additional setup.
- `DEBUG` is enabled in the current settings — suitable for development only.
- Never commit your `.env` file or `SECRET_KEY` to version control.

---

## Future Improvements

- Switch to PostgreSQL for production
- Add unit and integration tests with `pytest-django`
- Add Docker support for containerized deployment
- Deploy to Railway or Render
- Add note tags or recurring expense support
