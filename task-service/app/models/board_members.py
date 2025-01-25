from app.core.config import Base
from sqlalchemy import Column, String, DateTime,ForeignKey,UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func


class BoardMembers(Base):

    __tablename__ = "board_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    board_id = Column(UUID(as_uuid=True), ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True))
    role = Column(String(50), nullable=False,default = "MEMBER")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('board_id', 'user_id', name='unique_board_user'),
    )


