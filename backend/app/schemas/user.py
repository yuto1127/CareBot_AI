from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime

class UserCreate(BaseModel):
    """ユーザー作成スキーマ"""
    email: EmailStr = Field(..., description="メールアドレス")
    password: str = Field(..., min_length=8, description="パスワード（8文字以上）")
    name: str = Field(..., min_length=2, max_length=50, description="ユーザー名")

class UserResponse(BaseModel):
    """ユーザーレスポンススキーマ"""
    id: int
    email: str
    name: str
    plan_type: str
    created_at: str
    updated_at: Optional[str] = None

class UserUpdate(BaseModel):
    """ユーザー更新スキーマ"""
    name: Optional[str] = Field(None, min_length=2, max_length=50, description="ユーザー名")
    email: Optional[EmailStr] = Field(None, description="メールアドレス")
    plan_type: Optional[str] = Field(None, description="プランタイプ")

class UserProfile(BaseModel):
    """ユーザープロフィールスキーマ"""
    id: int
    email: str
    username: str
    plan_type: str
    created_at: str
    updated_at: Optional[str] = None

class UserProfileUpdate(BaseModel):
    """プロフィール更新スキーマ"""
    username: Optional[str] = Field(None, min_length=2, max_length=50, description="ユーザー名")
    email: Optional[EmailStr] = Field(None, description="メールアドレス")

class UserProfileResponse(BaseModel):
    """プロフィールレスポンススキーマ"""
    profile: UserProfile
    message: str

class UserStats(BaseModel):
    """ユーザー統計スキーマ"""
    total_journals: int
    total_moods: int
    total_cbt_sessions: int
    total_meditation_sessions: int
    total_sound_sessions: int
    total_pomodoro_sessions: int
    average_mood_score: Optional[float] = None
    last_activity: Optional[str] = None

class UserProfileWithStats(BaseModel):
    """統計付きプロフィールスキーマ"""
    profile: UserProfile
    stats: UserStats
    message: str

class PasswordChange(BaseModel):
    """パスワード変更スキーマ"""
    current_password: str = Field(..., description="現在のパスワード")
    new_password: str = Field(..., min_length=8, description="新しいパスワード（8文字以上）")

class PasswordChangeResponse(BaseModel):
    """パスワード変更レスポンススキーマ"""
    message: str
    success: bool

class AccountDelete(BaseModel):
    """アカウント削除スキーマ"""
    password: str = Field(..., description="確認用パスワード")

class AccountDeleteResponse(BaseModel):
    """アカウント削除レスポンススキーマ"""
    message: str
    success: bool 