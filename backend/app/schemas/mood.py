from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class MoodCreate(BaseModel):
    """気分記録作成スキーマ"""
    mood: int = Field(..., ge=1, le=5, description="気分スコア（1-5）")
    note: Optional[str] = Field(None, max_length=1000, description="メモ（1,000文字以下）")
    
    @validator('mood')
    def validate_mood(cls, v):
        """気分スコアの検証"""
        if not isinstance(v, int):
            raise ValueError('気分スコアは整数である必要があります')
        if v < 1 or v > 5:
            raise ValueError('気分スコアは1から5の間である必要があります')
        return v
    
    @validator('note')
    def validate_note(cls, v):
        """メモの検証"""
        if v is not None and len(v) > 1000:
            raise ValueError('メモは1,000文字以下である必要があります')
        return v

class MoodResponse(BaseModel):
    """気分記録レスポンススキーマ"""
    id: int
    user_id: int
    mood: int
    note: Optional[str]
    recorded_at: datetime
    
    class Config:
        from_attributes = True

class MoodUpdate(BaseModel):
    """気分記録更新スキーマ"""
    mood: Optional[int] = Field(None, ge=1, le=5, description="気分スコア（1-5）")
    note: Optional[str] = Field(None, max_length=1000, description="メモ（1,000文字以下）")
    
    @validator('mood')
    def validate_mood(cls, v):
        """気分スコアの検証"""
        if v is not None:
            if not isinstance(v, int):
                raise ValueError('気分スコアは整数である必要があります')
            if v < 1 or v > 5:
                raise ValueError('気分スコアは1から5の間である必要があります')
        return v
    
    @validator('note')
    def validate_note(cls, v):
        """メモの検証"""
        if v is not None and len(v) > 1000:
            raise ValueError('メモは1,000文字以下である必要があります')
        return v

class MoodListResponse(BaseModel):
    """気分記録一覧レスポンススキーマ"""
    moods: list[MoodResponse]
    total_count: int

class MoodStats(BaseModel):
    """気分統計スキーマ"""
    average_mood: float
    mood_trend: list[dict]
    stress_trend: list[dict]
    total_records: int 