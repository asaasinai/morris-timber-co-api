# Vercel Deployment Troubleshooting

## Common Issues and Solutions

### 500 Internal Server Error

If you're getting a 500 error, check the following:

1. **Database Connection**

   - Make sure `DATABASE_URL` environment variable is set in Vercel
   - SQLite will NOT work on Vercel - you MUST use PostgreSQL
   - Test your database connection string locally first

2. **Environment Variables**

   - Go to your Vercel project settings → Environment Variables
   - Ensure these are set:
     - `DATABASE_URL` - PostgreSQL connection string
     - `SESSION_SECRET_KEY` - A secure random string
     - `FRONTEND_URLS` - Your frontend domain(s)

3. **Check Vercel Logs**

   - Go to your Vercel dashboard → Your project → Functions tab
   - Click on a failed function to see detailed error logs
   - Look for database connection errors or missing environment variables

4. **Test Health Endpoint**
   - Try accessing: `https://your-api.vercel.app/health`
   - This endpoint doesn't require database access
   - If this works, the issue is likely database-related

### Database Setup Options

**Option 1: Vercel Postgres (Recommended)**

1. In Vercel dashboard, go to Storage tab
2. Create a new Postgres database
3. Copy the connection string
4. Set it as `DATABASE_URL` environment variable

**Option 2: Supabase (Free tier available)**

1. Create account at supabase.com
2. Create a new project
3. Get connection string from Settings → Database
4. Set as `DATABASE_URL` environment variable

**Option 3: Other PostgreSQL providers**

- Railway, Neon, Render, etc.
- Get connection string and set as `DATABASE_URL`

### Testing Locally with PostgreSQL

Before deploying, test with PostgreSQL locally:

```bash
# Install PostgreSQL locally or use Docker
docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres

# Set environment variable
export DATABASE_URL="postgresql://postgres:password@localhost:5432/morris_timber"

# Run the app
uv run uvicorn main:app --reload
```

### Generate Session Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Use this output as your `SESSION_SECRET_KEY` environment variable.
