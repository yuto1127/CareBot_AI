from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Dict, Any, List
from app.utils.auth import get_current_user
from app.database.supabase_db import SupabaseDB
from app.utils.logger import logger
from app.utils.error_handler import (
    ValidationError, DatabaseError,
    create_error_response, log_request_info, validate_required_fields
)
from app.schemas.user import UserUpdate
from pydantic import BaseModel

router = APIRouter(tags=["admin"])

class RoleUpdate(BaseModel):
    """ロール更新スキーマ"""
    user_id: int
    role: str
    reason: str = "管理者によるロール変更"

class UserRoleResponse(BaseModel):
    """ユーザーロールレスポンススキーマ"""
    user_id: int
    email: str
    name: str
    current_role: str
    plan_type: str
    updated_at: str

@router.get("/users", response_model=List[UserRoleResponse])
def get_all_users(current_user: dict = Depends(get_current_user), request: Request = None):
    """すべてのユーザーを取得（管理者のみ）"""
    try:
        if request:
            log_request_info(request, current_user['id'])

        # 管理者権限チェック
        if current_user.get('role') != 'admin':
            raise HTTPException(status_code=403, detail="管理者権限が必要です")

        # すべてのユーザーを取得
        users = SupabaseDB.get_all_users()
        
        logger.log_user_action(
            user_id=current_user['id'],
            action="admin_get_all_users"
        )

        return users

    except DatabaseError as e:
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error("管理者ユーザー取得エラー", e, {"admin_id": current_user['id']})
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail="ユーザー取得に失敗しました")

@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    role_data: RoleUpdate,
    current_user: dict = Depends(get_current_user),
    request: Request = None
):
    """ユーザーのロールを更新（管理者のみ）"""
    try:
        if request:
            log_request_info(request, current_user['id'])

        # 管理者権限チェック
        if current_user.get('role') != 'admin':
            raise HTTPException(status_code=403, detail="管理者権限が必要です")

        # バリデーション
        validate_required_fields(role_data.dict(), ['user_id', 'role'])
        
        # 有効なロールかチェック
        valid_roles = ['authenticated', 'admin', 'premium', 'moderator']
        if role_data.role not in valid_roles:
            raise ValidationError(f"無効なロールです。有効なロール: {valid_roles}")

        # ユーザーが存在するかチェック
        target_user = SupabaseDB.get_user_by_id(user_id)
        if not target_user:
            raise ValidationError("指定されたユーザーが見つかりません")

        # ロール更新
        updated_user = SupabaseDB.update_user_role(
            user_id=user_id,
            role=role_data.role,
            updated_by=current_user['id'],
            reason=role_data.reason
        )

        if not updated_user:
            raise DatabaseError("ロールの更新に失敗しました")

        logger.log_user_action(
            user_id=current_user['id'],
            action="admin_update_user_role",
            details={
                "target_user_id": user_id,
                "new_role": role_data.role,
                "reason": role_data.reason
            }
        )

        return {
            "message": f"ユーザー {target_user['email']} のロールを {role_data.role} に更新しました",
            "user": updated_user
        }

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
        logger.error("ロール更新エラー", e, {"admin_id": current_user['id'], "target_user_id": user_id})
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail="ロール更新に失敗しました")

@router.get("/users/{user_id}/role")
def get_user_role(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    request: Request = None
):
    """ユーザーのロールを取得（管理者のみ）"""
    try:
        if request:
            log_request_info(request, current_user['id'])

        # 管理者権限チェック
        if current_user.get('role') != 'admin':
            raise HTTPException(status_code=403, detail="管理者権限が必要です")

        # ユーザー情報を取得
        user = SupabaseDB.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

        logger.log_user_action(
            user_id=current_user['id'],
            action="admin_get_user_role",
            details={"target_user_id": user_id}
        )

        return {
            "user_id": user['id'],
            "email": user['email'],
            "name": user['name'],
            "role": user.get('role', 'authenticated'),
            "plan_type": user.get('plan_type', 'free')
        }

    except DatabaseError as e:
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error("ロール取得エラー", e, {"admin_id": current_user['id'], "target_user_id": user_id})
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail="ロール取得に失敗しました") 