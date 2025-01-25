from app.core.config import Base
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey,Enum as SQLAlchemyEnum,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func
from enum import Enum

class TaskStatus(str,Enum):
    
    to_do = "to_do"
    in_progress = "in_progress"
    done = "done"

class Task(Base):

    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    board_id = Column(UUID(as_uuid=True), ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    task_name = Column(String(250),unique = True,nullable = False)
    description = Column(String(500))
    status = Column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.to_do, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


