from pydantic import BaseModel, Field, EmailStr,validator
from typing import Optional, Dict
import uuid
import re

class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8) 
   
    @validator('password')
    def validate_password(cls,v):
        if not re.search(r"[0-9]",v):
         raise ValueError("Password must contain at least one number.")
        if not re.search(r"[!@#$%^&*()_+={}|\[\]:;<>,.?/~`]", v):
            raise ValueError("Password must contain at least one symbol.")
        return v

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
  
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str
   
    class Config:
       from_attributes = True #tells pydantic to read data even if its returned from orm


class LoginRequest(BaseModel):
    email: str
    password: str
        

