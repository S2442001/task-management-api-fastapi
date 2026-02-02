import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base 
from sqlalchemy.orm import relationship 

class User(Base):

    __tablename__="users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True) 
    email=Column(String, unique=True, nullable=False)
    hashed_password=Column(String, nullable=False)
    role=Column(String) # user or admin 
    tasks=relationship("Task", back_populates="owner")


