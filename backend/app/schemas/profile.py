from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ProfileCreate(BaseModel):
    """プロフィール作成スキーマ"""
    avatar_url: Optional[str] = Field(None, description="アバター画像URL")
    bio: Optional[str] = Field(None, max_length=500, description="自己紹介（500文字以下）")
    preferences: Optional[Dict[str, Any]] = Field(None, description="ユーザー設定")

class ProfileUpdate(BaseModel):
    """プロフィール更新スキーマ"""
    avatar_url: Optional[str] = Field(None, description="アバター画像URL")
    bio: Optional[str] = Field(None, max_length=500, description="自己紹介（500文字以下）")
    preferences: Optional[Dict[str, Any]] = Field(None, description="ユーザー設定")

class ProfileResponse(BaseModel):
    """プロフィールレスポンススキーマ"""
    id: int
    user_id: int
    avatar_url: Optional[str]
    bio: Optional[str]
    preferences: Optional[Dict[str, Any]]
    created_at: str
    updated_at: Optional[str]

    class Config:
        from_attributes = True 