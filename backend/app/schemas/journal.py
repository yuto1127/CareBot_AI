from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime

class JournalCreate(BaseModel):
    """ジャーナル作成スキーマ"""
    content: str = Field(..., min_length=10, max_length=10000, description="ジャーナル内容（10文字以上10,000文字以下）")
    
    @validator('content')
    def validate_content(cls, v):
        """ジャーナル内容の検証"""
        if not v or not v.strip():
            raise ValueError('ジャーナル内容は空にできません')
        if len(v.strip()) < 10:
            raise ValueError('ジャーナル内容は10文字以上である必要があります')
        if len(v) > 10000:
            raise ValueError('ジャーナル内容は10,000文字以下である必要があります')
        return v

class JournalUpdate(BaseModel):
    """ジャーナル更新スキーマ"""
    content: str = Field(..., min_length=10, max_length=10000, description="ジャーナル内容（10文字以上10,000文字以下）")
    
    @validator('content')
    def validate_content(cls, v):
        """ジャーナル内容の検証"""
        if not v or not v.strip():
            raise ValueError('ジャーナル内容は空にできません')
        if len(v.strip()) < 10:
            raise ValueError('ジャーナル内容は10文字以上である必要があります')
        if len(v) > 10000:
            raise ValueError('ジャーナル内容は10,000文字以下である必要があります')
        return v

class JournalResponse(BaseModel):
    """ジャーナルレスポンススキーマ"""
    id: int
    user_id: int
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class JournalListResponse(BaseModel):
    """ジャーナル一覧レスポンススキーマ"""
    journals: list[JournalResponse]
    total_count: int 