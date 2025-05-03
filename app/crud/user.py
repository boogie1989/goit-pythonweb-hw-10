"""
CRUD operations for users.
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.auth.security import get_password_hash


def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> Optional[User]:
    """
    Get a user by ID.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get a user by email.
    """
    return db.query(User).filter(User.email == email).first()





def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    db_user = get_user(db, user_id)
    if db_user and user_data.email:
        db_user.email = user_data.email
        db.commit()
        db.refresh(db_user)
    return db_user


def update_user_avatar(db: Session, user_id: int, avatar_url: str) -> Optional[User]:
    db_user = get_user(db, user_id)
    if db_user:
        db_user.avatar_url = avatar_url
        db.commit()
        db.refresh(db_user)
    return db_user


def verify_user(db: Session, user_id: int) -> Optional[User]:
    """
    Mark a user as verified.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.is_verified = True
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> Optional[User]:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
