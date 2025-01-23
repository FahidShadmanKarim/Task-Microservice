from app.core.config import Base
from sqlalchemy import Column,String,Integer,DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func


class User(Base):
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50),unique = True, nullable = False)
    email = Column(String(100),unique = True,nullable = False)
    hashed_password = Column(String(255),nullable = False)
    created_at = Column(DateTime, server_default=func.now())  
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now()) 

    



