from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MoodCreate(BaseModel):
    """気分記録作成スキーマ"""
    mood: int = Field(..., ge=1, le=10, description="気分スコア（1-10）")
    notes: Optional[str] = Field(None, max_length=500, description="メモ")
    activities: Optional[list] = Field(default=[], description="活動リスト")
    stress_level: Optional[int] = Field(None, ge=1, le=10, description="ストレスレベル（1-10）")

class MoodUpdate(BaseModel):
    """気分記録更新スキーマ"""
    mood: Optional[int] = Field(None, ge=1, le=10, description="気分スコア（1-10）")
    notes: Optional[str] = Field(None, max_length=500, description="メモ")
    activities: Optional[list] = Field(None, description="活動リスト")
    stress_level: Optional[int] = Field(None, ge=1, le=10, description="ストレスレベル（1-10）")

class MoodResponse(BaseModel):
    """気分記録レスポンススキーマ"""
    id: int
    user_id: int
    mood: int
    notes: Optional[str]
    activities: Optional[list]
    stress_level: Optional[int]
    created_at: str

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