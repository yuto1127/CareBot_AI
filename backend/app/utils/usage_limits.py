from typing import Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.supabase_db import SupabaseDB

# プラン別使用回数制限
USAGE_LIMITS = {
    "free": {
        "journal": 10,
        "mood": 20,
        "ai_analysis": 5,
        "cbt_session": 3,
        "meditation_session": 5,
        "sound_play": 20,
        "pomodoro_session": 10
    },
    "premium": {
        "journal": 1000,
        "mood": 2000,
        "ai_analysis": 100,
        "cbt_session": 50,
        "meditation_session": 100,
        "sound_play": 500,
        "pomodoro_session": 200
    }
}

def get_usage_limit(plan_type: str, feature: str) -> int:
    """プランと機能に基づいて使用回数制限を取得"""
    return USAGE_LIMITS.get(plan_type, USAGE_LIMITS["free"]).get(feature, 0)

def get_current_usage(user_id: int, feature: str) -> int:
    """現在の使用回数を取得"""
    usage_record = SupabaseDB.get_usage_count(user_id, feature)
    return usage_record['usage_count'] if usage_record else 0

def can_use_feature(user_id: int, feature: str) -> dict:
    """機能を使用できるかチェック"""
    user = SupabaseDB.get_user_by_id(user_id)
    if not user:
        return {"can_use": False, "current_usage": 0, "limit": 0, "plan_type": "free"}
    
    plan_type = user.get('plan_type', 'free')
    limit = get_usage_limit(plan_type, feature)
    current_usage = get_current_usage(user_id, feature)
    
    return {
        "can_use": current_usage < limit,
        "current_usage": current_usage,
        "limit": limit,
        "plan_type": plan_type
    }

def increment_usage(user_id: int, feature: str):
    """使用回数を増加"""
    SupabaseDB.create_or_update_usage(user_id, feature, 1) 