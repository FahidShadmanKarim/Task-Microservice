from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.config import get_db  # Dependency for DB session
from app.crud.user_crud import create_user,get_users,get_user_by_id,update_user,delete_user
from app.schemas.user_schema import UserCreate,UserResponse,UserUpdate
from fastapi_pagination import Page
from typing import List

router = APIRouter()

@router.post("/users",response_model=UserResponse)
def create_user_endpoint(user_create:UserCreate,db:Session = Depends(get_db)):

    user = create_user(db,user_create)
    return user

@router.get("/users", response_model=Page[UserResponse])
def get_users_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    return get_users(db)


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id_endpoint(user_id: int, db: Session = Depends(get_db)):

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):

    user = update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}", response_model=None)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    result = delete_user(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}