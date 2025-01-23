from fastapi import  Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from typing import Optional, List
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
import bcrypt

def create_user(db: Session, user: UserCreate) -> UserResponse:
    
    db_user = db.query(User).filter(User.email == user.email).first()

    if db_user:
        raise HTTPException(status_code = 400,detail = "Email already registered")

    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,  # Ensure password is hashed before calling this function
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponse.from_orm(db_user)

def get_user_by_id(db: Session, user_id: int) -> Optional[UserResponse]:
  
    user = db.query(User).filter(User.id == user_id).first()
    return UserResponse.from_orm(user) if user else None

def get_users(db: Session) -> Page[UserResponse]:
    query = db.query(User)
    users = paginate(query)
    return users

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[UserResponse]:

    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return UserResponse.from_orm(db_user)

def delete_user(db: Session, user_id: int) -> bool:
  
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True
