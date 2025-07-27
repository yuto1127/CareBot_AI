from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AnalysisRequest(BaseModel):
    journal_ids: Optional[List[int]] = None
    mood_ids: Optional[List[int]] = None
    analysis_type: str = "general"  # "general", "mood_trend", "stress_analysis"

class AnalysisResponse(BaseModel):
    id: int
    user_id: int
    analysis_type: str
    summary: str
    insights: List[str]
    recommendations: List[str]
    mood_score: Optional[float] = None
    stress_level: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True 