from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from app.schemas.mood import MoodCreate, MoodResponse
from app.utils.auth import get_current_user
from app.utils.usage_limits import can_use_feature, increment_usage
from app.database.supabase_db import SupabaseDB
from app.utils.logger import logger
from app.utils.error_handler import (
    ValidationError, DatabaseError, UsageLimitError,
    create_error_response, log_request_info, validate_required_fields
)

router = APIRouter(tags=["moods"])

def validate_mood_score(mood: int) -> bool:
    """気分スコアのバリデーション"""
    return 1 <= mood <= 5

def validate_mood_note(note: str) -> bool:
    """気分メモのバリデーション"""
    if note is None:
        return True
    if len(note) > 1000:  # 最大1,000文字
        return False
    return True

@router.get("/", response_model=List[MoodResponse])
def get_moods(current_user: dict = Depends(get_current_user), request: Request = None):
    """ユーザーの気分記録一覧を取得"""
    try:
        if request:
            log_request_info(request, current_user['id'])
        
        moods = SupabaseDB.get_user_moods(current_user['id'])
        if moods is None:
            raise DatabaseError("気分記録の取得に失敗しました")
        
        logger.log_user_action(
            user_id=current_user['id'],
            action="get_moods",
            details={"count": len(moods)}
        )
        
        return moods
        
    except DatabaseError as e:
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error("気分記録取得エラー", e, {"user_id": current_user['id']})
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail="気分記録の取得に失敗しました")

@router.post("/", response_model=MoodResponse)
def create_mood(
    mood_data: MoodCreate,
    current_user: dict = Depends(get_current_user),
    request: Request = None
):
    """気分記録を作成"""
    try:
        if request:
            log_request_info(request, current_user['id'])
        
        # バリデーション
        validate_required_fields(mood_data.dict(), ['mood'])
        
        # 気分スコアの検証
        if not validate_mood_score(mood_data.mood):
            raise ValidationError("気分スコアは1から5の間である必要があります")
        
        # メモの検証
        if mood_data.note and not validate_mood_note(mood_data.note):
            raise ValidationError("メモは1,000文字以下である必要があります")
        
        # 使用回数制限をチェック
        usage_check = can_use_feature(current_user['id'], "mood")
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
        
        # 気分記録作成
        db_mood = SupabaseDB.create_mood(current_user['id'], mood_data)
        if not db_mood:
            raise DatabaseError("気分記録の作成に失敗しました")
        
        # 使用回数を増加
        increment_usage(current_user['id'], "mood")
        
        # 成功ログ
        logger.log_user_action(
            user_id=current_user['id'],
            action="create_mood",
            details={"mood_id": db_mood['id'], "mood_score": db_mood['mood']}
        )
        
        return db_mood
        
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
        logger.error("気分記録作成エラー", e, {"user_id": current_user['id']})
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail="気分記録の作成に失敗しました")

@router.delete("/{mood_id}")
def delete_mood(
    mood_id: int,
    current_user: dict = Depends(get_current_user),
    request: Request = None
):
    """気分記録を削除"""
    try:
        if request:
            log_request_info(request, current_user['id'])
        
        # 気分記録IDの検証
        if mood_id <= 0:
            raise ValidationError("無効な気分記録IDです")
        
        success = SupabaseDB.delete_mood(mood_id, current_user['id'])
        if not success:
            raise HTTPException(status_code=404, detail="気分記録が見つかりません")
        
        # 成功ログ
        logger.log_user_action(
            user_id=current_user['id'],
            action="delete_mood",
            details={"mood_id": mood_id}
        )
        
        return {"message": "気分記録を削除しました"}
        
    except ValidationError as e:
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("気分記録削除エラー", e, {"user_id": current_user['id'], "mood_id": mood_id})
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail="気分記録の削除に失敗しました") 