# Morris Timber Co Backend API

FastAPI backend for Morris Timber Co website.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Environment Variables

- `DATABASE_URL`: Database connection string (defaults to SQLite: `sqlite:///./morris_timber.db`)

## Features

- Cookie-based session authentication
- CORS enabled for frontend integration
- SQLite database (easily switchable to PostgreSQL/MySQL)
- Password hashing with bcrypt
- RESTful API endpoints for:
  - Authentication (login, register, logout)
  - Products
  - Team Members
  - Story Panels
  - Site Settings
  - Contact Messages

## Important Notes

- Change the session secret key in `main.py` before deploying to production
- Update CORS origins in `main.py` to match your frontend URL
- The database file (`morris_timber.db`) will be created automatically on first run
