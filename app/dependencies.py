from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth import get_current_user_from_session

security = HTTPBearer()


def get_current_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
):
    """Dependency to get the current authenticated user"""
    return current_user


def get_optional_user(
    db: Session = Depends(get_db),
):
    """Dependency to optionally get the current user (returns None if not authenticated)"""
    try:
        return get_current_user_from_session(db)
    except:
        return None

