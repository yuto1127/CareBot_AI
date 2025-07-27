from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.mood import MoodCreate, MoodResponse
from app.utils.auth import get_current_user
from app.utils.usage_limits import can_use_feature, increment_usage
from app.database.supabase_db import SupabaseDB

router = APIRouter()

@router.get("/", response_model=List[MoodResponse])
def get_moods(current_user: dict = Depends(get_current_user)):
    moods = SupabaseDB.get_user_moods(current_user['id'])
    return moods

@router.post("/", response_model=MoodResponse)
def create_mood(
    mood: MoodCreate,
    current_user: dict = Depends(get_current_user)
):
    # 使用回数制限をチェック
    usage_check = can_use_feature(current_user['id'], "mood")
    if not usage_check["can_use"]:
        raise HTTPException(
            status_code=429,
            detail={
                "message": "使用回数制限に達しました",
                "current_usage": usage_check["current_usage"],
                "limit": usage_check["limit"],
                "plan_type": usage_check["plan_type"],
                "upgrade_required": True
            }
        )
    
    db_mood = SupabaseDB.create_mood(current_user['id'], mood)
    if not db_mood:
        raise HTTPException(
            status_code=500,
            detail="Failed to create mood record"
        )
    
    # 使用回数を増加
    increment_usage(current_user['id'], "mood")
    
    return db_mood 