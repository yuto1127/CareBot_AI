from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    analysis_type = Column(String(50), nullable=False)  # "general", "mood_trend", "stress_analysis"
    summary = Column(Text, nullable=False)
    insights = Column(Text, nullable=False)  # JSON string
    recommendations = Column(Text, nullable=False)  # JSON string
    mood_score = Column(Float, nullable=True)
    stress_level = Column(String(20), nullable=True)  # "low", "medium", "high"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーションシップ
    user = relationship("User", back_populates="analyses") 