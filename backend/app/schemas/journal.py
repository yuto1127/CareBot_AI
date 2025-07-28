from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class JournalCreate(BaseModel):
    """ジャーナル作成スキーマ"""
    content: str = Field(..., min_length=1, description="ジャーナル内容")
    title: Optional[str] = Field(None, max_length=200, description="タイトル")
    mood_score: Optional[int] = Field(None, ge=1, le=10, description="気分スコア（1-10）")
    tags: Optional[list] = Field(default=[], description="タグ")

class JournalUpdate(BaseModel):
    """ジャーナル更新スキーマ"""
    content: Optional[str] = Field(None, min_length=1, description="ジャーナル内容")
    title: Optional[str] = Field(None, max_length=200, description="タイトル")
    mood_score: Optional[int] = Field(None, ge=1, le=10, description="気分スコア（1-10）")
    tags: Optional[list] = Field(None, description="タグ")

class JournalResponse(BaseModel):
    """ジャーナルレスポンススキーマ"""
    id: int
    user_id: int
    content: str
    title: Optional[str]
    mood_score: Optional[int]
    tags: Optional[list]
    created_at: str
    updated_at: Optional[str]

class JournalListResponse(BaseModel):
    """ジャーナル一覧レスポンススキーマ"""
    journals: list[JournalResponse]
    total_count: int 