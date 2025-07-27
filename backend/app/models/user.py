from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String, nullable=True)
    plan_type = Column(String, default="free")  # "free" or "premium"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # リレーションシップ
    journals = relationship("Journal", back_populates="user")
    moods = relationship("Mood", back_populates="user")
    usage_records = relationship("Usage", back_populates="user")
    analyses = relationship("Analysis", back_populates="user") 