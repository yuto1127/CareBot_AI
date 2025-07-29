from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Dict, Any
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from app.utils.auth import get_current_user
from app.database.supabase_db import SupabaseDB
from app.utils.logger import logger
from app.utils.error_handler import (
    ValidationError, DatabaseError,
    create_error_response, log_request_info, validate_required_fields
)

router = APIRouter(tags=["profiles"])

@router.get("/me", response_model=ProfileResponse)
def get_my_profile(current_user: dict = Depends(get_current_user), request: Request = None):
    """自分のプロフィールを取得"""
    try:
        if request:
            log_request_info(request, current_user['id'])

        profile = SupabaseDB.get_user_profile(current_user['id'])
        if not profile:
            raise HTTPException(status_code=404, detail="プロフィールが見つかりません")

        logger.log_user_action(
            user_id=current_user['id'],
            action="get_profile"
        )

        return profile

    except DatabaseError as e:
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error("プロフィール取得エラー", e, {"user_id": current_user['id']})
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail="プロフィールの取得に失敗しました")

@router.post("/me", response_model=ProfileResponse)
def create_my_profile(
    profile_data: ProfileCreate,
    current_user: dict = Depends(get_current_user),
    request: Request = None
):
    """自分のプロフィールを作成"""
    try:
        if request:
            log_request_info(request, current_user['id'])

        # 既存のプロフィールをチェック
        existing_profile = SupabaseDB.get_user_profile(current_user['id'])
        if existing_profile:
            raise ValidationError("プロフィールは既に存在します")

        # プロフィール作成
        profile = SupabaseDB.create_user_profile(current_user['id'], profile_data.dict())
        if not profile:
            raise DatabaseError("プロフィールの作成に失敗しました")

        logger.log_user_action(
            user_id=current_user['id'],
            action="create_profile"
        )

        return profile

    except ValidationError as e:
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error("プロフィール作成エラー", e, {"user_id": current_user['id']})
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail="プロフィールの作成に失敗しました")

@router.put("/me", response_model=ProfileResponse)
def update_my_profile(
    profile_data: ProfileUpdate,
    current_user: dict = Depends(get_current_user),
    request: Request = None
):
    """自分のプロフィールを更新"""
    try:
        if request:
            log_request_info(request, current_user['id'])

        # 既存のプロフィールをチェック
        existing_profile = SupabaseDB.get_user_profile(current_user['id'])
        if not existing_profile:
            raise ValidationError("プロフィールが存在しません")

        # プロフィール更新
        profile = SupabaseDB.update_user_profile(current_user['id'], profile_data.dict(exclude_unset=True))
        if not profile:
            raise DatabaseError("プロフィールの更新に失敗しました")

        logger.log_user_action(
            user_id=current_user['id'],
            action="update_profile"
        )

        return profile

    except ValidationError as e:
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error("プロフィール更新エラー", e, {"user_id": current_user['id']})
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail="プロフィールの更新に失敗しました") 