from app.core.config import Base
from sqlalchemy import Column,String,Integer,DataTime,Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchem.sql import func
from enum import Enum

class TaskStatus(str,Enum):
    pending = "pending"
    completed = "completed"

class Task(Base):

    __tablename__ = "tasks"

    id = Column(UUID(as_uuid) =True,primary_key=True,default=uuid.uuid4)
    task_name = Column(String(250),unique = True,nullable = False)
    description = Column(String(500))
    status = Column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.pending)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


