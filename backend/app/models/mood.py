from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Mood(Base):
    __tablename__ = "moods"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    mood = Column(Integer, nullable=False)  # 1-5 scale
    note = Column(Text, nullable=True)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーションシップ
    user = relationship("User", back_populates="moods") 