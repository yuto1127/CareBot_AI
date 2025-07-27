from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...models.database import get_db
from ...models.user import User
from ...utils.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

class UserResponse(BaseModel):
    id: int
    email: str
    name: str = None
    plan_type: str
    created_at: str
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ユーザー一覧を取得（管理者用）"""
    users = db.query(User).all()
    return users

@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """現在のユーザー情報を取得"""
    return current_user 