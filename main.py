from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
from app.database import engine, Base
from app.routers import (
    auth,
    products,
    team_members,
    story_panels,
    site_settings,
    contact_messages,
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Morris Timber Co API", version="1.0.0")

# Get secret key from environment variable or use default (for development)
SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "your-secret-key-change-this-in-production")

# Add session middleware (must be before CORS)
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=86400,  # 24 hours
    same_site="lax",
)

FRONTEND_URLS = os.getenv("FRONTEND_URLS", "http://localhost:3000,http://localhost:5173,http://localhost:8080").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_URLS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(products.router, prefix="/api", tags=["Products"])
app.include_router(team_members.router, prefix="/api", tags=["Team Members"])
app.include_router(story_panels.router, prefix="/api", tags=["Story Panels"])
app.include_router(site_settings.router, prefix="/api", tags=["Site Settings"])
app.include_router(contact_messages.router, prefix="/api", tags=["Contact Messages"])


@app.get("/")
async def root():
    return {"message": "Morris Timber Co API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

