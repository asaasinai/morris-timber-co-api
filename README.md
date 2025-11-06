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

- `DATABASE_URL`: Database connection string
  - Local development: `sqlite:///./morris_timber.db` (default)
  - Production/Vercel: PostgreSQL connection string (e.g., `postgresql://user:pass@host/dbname`)
- `SESSION_SECRET_KEY`: Secret key for session cookies (required in production)
- `FRONTEND_URLS`: Comma-separated list of allowed frontend URLs for CORS (defaults to localhost URLs)

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

## Vercel Deployment

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Set the following environment variables in Vercel:
   - `DATABASE_URL`: Your PostgreSQL connection string (SQLite won't work on Vercel)
   - `SESSION_SECRET_KEY`: A secure random string for session encryption
   - `FRONTEND_URLS`: Your frontend domain(s), e.g., `https://your-frontend.vercel.app`
4. Deploy!

**Note:** SQLite doesn't work on Vercel's serverless functions. You'll need to use PostgreSQL (Vercel Postgres, Supabase, or another provider).

## Important Notes

- SQLite is fine for local development, but use PostgreSQL for production/Vercel
- Set `SESSION_SECRET_KEY` environment variable in production (don't use the default)
- Set `FRONTEND_URLS` environment variable to include your production frontend URL
- The database file (`morris_timber.db`) will be created automatically on first run (local only)
