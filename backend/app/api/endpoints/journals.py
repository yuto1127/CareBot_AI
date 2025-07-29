from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from app.schemas.journal import JournalCreate, JournalResponse
from app.utils.auth import get_current_user
from app.utils.usage_limits import can_use_feature, increment_usage
from app.database.supabase_db import SupabaseDB
from app.utils.logger import logger
from app.utils.error_handler import (
    ValidationError, DatabaseError, UsageLimitError,
    create_error_response, log_request_info, validate_required_fields
)

router = APIRouter(tags=["journals"])

def validate_journal_content(content: str) -> bool:
    """ジャーナル内容のバリデーション"""
    if not content or not content.strip():
        return False
    if len(content.strip()) < 10:
        return False
    if len(content) > 10000:  # 最大10,000文字
        return False
    return True

@router.get("/", response_model=List[JournalResponse])
def get_journals(current_user: dict = Depends(get_current_user), request: Request = None):
    """ユーザーのジャーナル一覧を取得"""
    try:
        if request:
            log_request_info(request, current_user['id'])
        
        journals = SupabaseDB.get_user_journals(current_user['id'])
        if journals is None:
            raise DatabaseError("ジャーナルの取得に失敗しました")
        
        logger.log_user_action(
            user_id=current_user['id'],
            action="get_journals",
            details={"count": len(journals)}
        )
        
        return journals
        
    except DatabaseError as e:
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error("ジャーナル取得エラー", e, {"user_id": current_user['id']})
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail="ジャーナルの取得に失敗しました")

@router.post("/", response_model=JournalResponse)
def create_journal(
    journal: JournalCreate,
    current_user: dict = Depends(get_current_user),
    request: Request = None
):
    """ジャーナルを作成"""
    try:
        if request:
            log_request_info(request, current_user['id'])
        
        # バリデーション
        validate_required_fields(journal.dict(), ['content'])
        
        # ジャーナル内容の検証
        if not validate_journal_content(journal.content):
            raise ValidationError("ジャーナル内容は10文字以上10,000文字以下である必要があります")
        
        # 使用回数制限をチェック
        usage_check = can_use_feature(current_user['id'], "journal")
        if not usage_check["can_use"]:
            raise UsageLimitError(
                "使用回数制限に達しました",
                {
                    "current_usage": usage_check["current_usage"],
                    "limit": usage_check["limit"],
                    "plan_type": usage_check["plan_type"],
                    "upgrade_required": True
                }
            )
        
        # ジャーナル作成
        db_journal = SupabaseDB.create_journal(current_user['id'], journal)
        if not db_journal:
            raise DatabaseError("ジャーナルの作成に失敗しました")
        
        # 使用回数を増加
        increment_usage(current_user['id'], "journal")
        
        # 成功ログ
        logger.log_user_action(
            user_id=current_user['id'],
            action="create_journal",
            details={"journal_id": db_journal['id']}
        )
        
        return db_journal
        
    except ValidationError as e:
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except UsageLimitError as e:
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=429, detail=str(e))
    except DatabaseError as e:
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error("ジャーナル作成エラー", e, {"user_id": current_user['id']})
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail="ジャーナルの作成に失敗しました")

@router.delete("/{journal_id}")
def delete_journal(
    journal_id: int,
    current_user: dict = Depends(get_current_user),
    request: Request = None
):
    """ジャーナルを削除"""
    try:
        if request:
            log_request_info(request, current_user['id'])
        
        # ジャーナルIDの検証
        if journal_id <= 0:
            raise ValidationError("無効なジャーナルIDです")
        
        success = SupabaseDB.delete_journal(journal_id, current_user['id'])
        if not success:
            raise HTTPException(status_code=404, detail="ジャーナルが見つかりません")
        
        # 成功ログ
        logger.log_user_action(
            user_id=current_user['id'],
            action="delete_journal",
            details={"journal_id": journal_id}
        )
        
        return {"message": "ジャーナルを削除しました"}
        
    except ValidationError as e:
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("ジャーナル削除エラー", e, {"user_id": current_user['id'], "journal_id": journal_id})
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail="ジャーナルの削除に失敗しました") 