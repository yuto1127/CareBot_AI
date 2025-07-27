from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...models.database import get_db
from ...models.user import User
from ...utils.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

class ProfileResponse(BaseModel):
    id: int
    user_id: int
    display_name: str = None
    avatar_url: str = None
    bio: str = None
    created_at: str
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[ProfileResponse])
def get_profiles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """プロフィール一覧を取得"""
    # 簡易実装のため、現在は空のリストを返す
    return []

@router.get("/me", response_model=ProfileResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """現在のユーザーのプロフィールを取得"""
    # 簡易実装のため、ダミーデータを返す
    return {
        "id": 1,
        "user_id": current_user.id,
        "display_name": current_user.name,
        "avatar_url": None,
        "bio": None,
        "created_at": current_user.created_at.isoformat()
    } 