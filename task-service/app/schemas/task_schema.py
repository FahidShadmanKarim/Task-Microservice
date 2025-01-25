from pydantic import BaseModel, Field,validator
from typing import Optional, Dict
import uuid
from uuid import UUID
from enum import Enum
import re
from datetime import datetime
from app.models.task_model import TaskStatus

   
class TaskCreate(BaseModel):
    task_name: str = Field(..., min_length=1, max_length=250)
    user_id: UUID
    board_id:UUID
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.to_do
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
       from_attributes = True

class TaskUpdate(BaseModel):
    task_name: Optional[str] = Field(None, max_length=250)
    description: Optional[str] = None
    status: Optional[TaskStatus]
    user_id: Optional[UUID]

    class Config:
        from_attributes = True

class TaskResponse(BaseModel):
    id: UUID
    board_id: UUID
    task_name: str
    description: Optional[str]
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
