from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, LoginRequest
from app.auth import get_password_hash, verify_password, get_current_user_from_session

router = APIRouter()


@router.get("/user")
async def get_user(
    request: Request,
    db: Session = Depends(get_db),
):
    """Get current user if authenticated, otherwise return null"""
    try:
        user = get_current_user_from_session(request, db)
        return user
    except HTTPException:
        return JSONResponse(content=None, status_code=200)


@router.post("/login", response_model=UserResponse)
async def login(
    login_data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """Login user and set session cookie"""
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    # Set session
    request.session["user_id"] = user.id
    
    return user


@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    """Register a new user"""
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Set session
    request.session["user_id"] = new_user.id
    
    # Return user with hashed password (as per API spec)
    return new_user


@router.post("/logout")
async def logout(request: Request):
    """Logout user and clear session cookie"""
    request.session.clear()
    return Response(status_code=status.HTTP_200_OK)

