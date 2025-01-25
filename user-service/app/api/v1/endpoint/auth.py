from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.config import get_db  # Dependency for DB session
from app.core.security import verify_password,create_access_token,verify_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.user_model import User
from datetime import timedelta
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/auth/login")
router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/auth/login")
def login(
    form_data: LoginRequest,
    db: Session = Depends(get_db)
):  
    print("Received form data:", form_data.username, form_data.password)
    print("Form data:", form_data)
    print("Username:", form_data.username)
    print("Password:", form_data.password)
    # Query the database for the user
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create a JWT access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
