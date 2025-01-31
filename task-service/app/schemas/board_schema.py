from pydantic import BaseModel, Field,validator
from typing import Optional, Dict
import uuid
from uuid import UUID
from enum import Enum
import re
from datetime import datetime


class BoardCreate(BaseModel):

    name: str
    description: Optional[str] = None
    created_by: UUID

    class Config:
      from_attributes = True

class BoardUpdate(BaseModel):

    name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
 
    class Config:
        from_attributes = True


class BoardResponse(BaseModel):
    id: UUID
    created_by:UUID
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
       from_attributes = True
    

class BoardAddUser(BaseModel):
    user_id: UUID
    role: str = "MEMBER"

