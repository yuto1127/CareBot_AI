from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, Any
import re

class UserRegister(BaseModel):
    """ユーザー登録スキーマ"""
    email: EmailStr = Field(..., description="メールアドレス")
    password: str = Field(..., min_length=8, description="パスワード（8文字以上）")
    username: str = Field(..., min_length=2, max_length=50, description="ユーザー名")
    plan_type: str = Field(default="free", description="プランタイプ")
    
    @validator('password')
    def validate_password(cls, v):
        """パスワードの強度を検証"""
        if len(v) < 8:
            raise ValueError('パスワードは8文字以上である必要があります')
        if not re.search(r'[A-Z]', v):
            raise ValueError('パスワードには大文字を含む必要があります')
        if not re.search(r'[a-z]', v):
            raise ValueError('パスワードには小文字を含む必要があります')
        if not re.search(r'\d', v):
            raise ValueError('パスワードには数字を含む必要があります')
        return v
    
    @validator('username')
    def validate_username(cls, v):
        """ユーザー名の形式を検証"""
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('ユーザー名は英数字とアンダースコアのみ使用できます')
        return v

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
    
    @validator('new_password')
    def validate_new_password(cls, v):
        """新しいパスワードの強度を検証"""
        if len(v) < 8:
            raise ValueError('パスワードは8文字以上である必要があります')
        if not re.search(r'[A-Z]', v):
            raise ValueError('パスワードには大文字を含む必要があります')
        if not re.search(r'[a-z]', v):
            raise ValueError('パスワードには小文字を含む必要があります')
        if not re.search(r'\d', v):
            raise ValueError('パスワードには数字を含む必要があります')
        return v

class UserUpdate(BaseModel):
    """ユーザー情報更新スキーマ"""
    username: Optional[str] = Field(None, min_length=2, max_length=50, description="ユーザー名")
    email: Optional[EmailStr] = Field(None, description="メールアドレス")
    
    @validator('username')
    def validate_username(cls, v):
        """ユーザー名の形式を検証"""
        if v is not None:
            if not re.match(r'^[a-zA-Z0-9_]+$', v):
                raise ValueError('ユーザー名は英数字とアンダースコアのみ使用できます')
        return v 