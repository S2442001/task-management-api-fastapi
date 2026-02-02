import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base 
from app.models.user import User
from sqlalchemy.orm import relationship

class Task(Base):

    __tablename__="tasks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True) 
    title=Column(String, unique=True, nullable=False)
    description=Column(String)
    status=Column(String, default="Pending") # In-Progress/Done
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    owner=relationship("User", back_populates="tasks")




