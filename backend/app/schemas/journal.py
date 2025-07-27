from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JournalBase(BaseModel):
    content: str

class JournalCreate(JournalBase):
    pass

class JournalResponse(JournalBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True 