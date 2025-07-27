from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MoodBase(BaseModel):
    mood: int
    note: Optional[str] = None

class MoodCreate(MoodBase):
    pass

class MoodResponse(MoodBase):
    id: int
    user_id: int
    recorded_at: datetime
    
    class Config:
        from_attributes = True 