from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Form
from sqlalchemy.orm import Session
from pydantic import EmailStr

from app.core.database import get_db
from app.core.email import send_verification_email
from app.schemas.user import UserCreate, UserResponse, Token, UserLogin
from app.crud.user import (
    create_user, get_user_by_email, verify_user
)
from app.auth.security import (
    verify_password, create_access_token, get_current_user, 
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.models.user import User
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    new_user = create_user(db, user)
    
    background_tasks.add_task(
        send_verification_email,
        new_user.email,
        new_user.id
    )
    
    return new_user


@router.post("/token", response_model=Token)
async def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, email)
    
    if user is None or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify/{user_id}/{verification_token}")
async def verify_email(user_id: int, verification_token: str, db: Session = Depends(get_db)):
    user = verify_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "Email verified successfully"}
