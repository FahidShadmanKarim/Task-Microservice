from pydantic import BaseModel, Field, EmailStr,validator
from typing import Optional, Dict
import uuid
from enum import Enum
import re
from app.models.task_model import TaskStatus

   
class TaskCreate(BaseModel):
    task_name: str = Field(..., min_length=1, max_length=250)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending
    user_id: UUID
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
       from_attributes = True


class TaskUpdate(BaseModel):
    task_name: Optional[str] = Field(None, max_length=250)
    description: Optional[str] = None
    status: Optional[TaskStatus]
    user_id: Optional[UUID]

    @validator('task_name', pre=True)
    def validate_task_name(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            return None
        return v

    @validator('status')
    def validate_status(cls, v):
        if v is None:
            return TaskStatus.pending
        if v not in TaskStatus:
            raise ValueError(f"Invalid status. Must be one of {', '.join(TaskStatus.values())}")
        return v

    class Config:
        from_attributes = True


class TaskResponse(BaseModel):
    id:uuid.UUID
    task_name:str
    description:str
    status:TaskStatus

    class Config:
        from_attributes = True
