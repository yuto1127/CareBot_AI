from fastapi import APIRouter, Depends
from typing import Dict, Any
from app.utils.auth import get_current_user
from app.utils.usage_limits import can_use_feature, get_usage_limit
from app.database.supabase_db import SupabaseDB

router = APIRouter(tags=["usage"])

@router.get("/status")
def get_usage_status(current_user: dict = Depends(get_current_user)):
    """ユーザーの使用回数状況を取得"""
    features = ["journal", "mood", "ai_analysis"]
    usage_status = {}
    
    for feature in features:
        usage_check = can_use_feature(current_user['id'], feature)
        usage_status[feature] = usage_check
    
    return {
        "user_id": current_user['id'],
        "plan_type": current_user.get('plan_type', 'free'),
        "usage": usage_status
    }

@router.get("/limits")
def get_plan_limits(current_user: dict = Depends(get_current_user)):
    """プラン別制限を取得"""
    plan_type = current_user.get('plan_type', 'free')
    limits = {}
    
    features = ["journal", "mood", "ai_analysis"]
    for feature in features:
        limits[feature] = get_usage_limit(plan_type, feature)
    
    return {
        "plan_type": plan_type,
        "limits": limits
    } 