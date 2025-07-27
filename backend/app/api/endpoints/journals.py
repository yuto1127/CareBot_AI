from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.journal import JournalCreate, JournalResponse
from app.utils.auth import get_current_user
from app.utils.usage_limits import can_use_feature, increment_usage
from app.database.supabase_db import SupabaseDB

router = APIRouter()

@router.get("/", response_model=List[JournalResponse])
def get_journals(current_user: dict = Depends(get_current_user)):
    journals = SupabaseDB.get_user_journals(current_user['id'])
    return journals

@router.post("/", response_model=JournalResponse)
def create_journal(
    journal: JournalCreate,
    current_user: dict = Depends(get_current_user)
):
    # 使用回数制限をチェック
    usage_check = can_use_feature(current_user['id'], "journal")
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
    
    db_journal = SupabaseDB.create_journal(current_user['id'], journal)
    if not db_journal:
        raise HTTPException(
            status_code=500,
            detail="Failed to create journal"
        )
    
    # 使用回数を増加
    increment_usage(current_user['id'], "journal")
    
    return db_journal

@router.delete("/{journal_id}")
def delete_journal(
    journal_id: int,
    current_user: dict = Depends(get_current_user)
):
    success = SupabaseDB.delete_journal(journal_id, current_user['id'])
    if not success:
        raise HTTPException(status_code=404, detail="Journal not found")
    
    return {"message": "Journal deleted"} 