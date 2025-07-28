from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any

class UserRegister(BaseModel):
    """ユーザー登録スキーマ"""
    email: EmailStr = Field(..., description="メールアドレス")
    password: str = Field(..., min_length=8, description="パスワード（8文字以上）")
    username: str = Field(..., min_length=2, max_length=50, description="ユーザー名")
    plan_type: str = Field(default="free", description="プランタイプ")

class UserLogin(BaseModel):
    """ユーザーログインスキーマ"""
    email: EmailStr = Field(..., description="メールアドレス")
    password: str = Field(..., description="パスワード")

class UserResponse(BaseModel):
    """ユーザーレスポンススキーマ"""
    user: Dict[str, Any]
    access_token: str
    token_type: str

class UserProfile(BaseModel):
    """ユーザープロフィールスキーマ"""
    id: int
    email: str
    username: str
    plan_type: str
    created_at: str
    updated_at: Optional[str] = None

class TokenData(BaseModel):
    """トークンデータスキーマ"""
    user_id: Optional[int] = None
    email: Optional[str] = None

class PasswordChange(BaseModel):
    """パスワード変更スキーマ"""
    current_password: str = Field(..., description="現在のパスワード")
    new_password: str = Field(..., min_length=8, description="新しいパスワード（8文字以上）")

class UserUpdate(BaseModel):
    """ユーザー情報更新スキーマ"""
    username: Optional[str] = Field(None, min_length=2, max_length=50, description="ユーザー名")
    email: Optional[EmailStr] = Field(None, description="メールアドレス") 