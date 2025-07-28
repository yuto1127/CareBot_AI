from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional
from ...database.supabase_db import SupabaseDB
from ...utils.logger import logger
from ...utils.error_handler import handle_carebot_error
from ...schemas.user import (
    UserProfile, UserProfileUpdate, UserProfileResponse,
    UserStats, UserProfileWithStats, PasswordChange,
    PasswordChangeResponse, AccountDelete, AccountDeleteResponse
)
from ...utils.auth import get_current_user
import bcrypt

router = APIRouter()

@router.get("/me", response_model=UserProfileResponse)
async def get_my_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
    """現在のユーザーのプロフィールを取得"""
    try:
        logger.info(f"プロフィール取得開始 - ユーザーID: {current_user['id']}")
        
        db = SupabaseDB()
        
        # ユーザー情報を取得
        user_data = db.get_user_by_id(current_user['id'])
        
        if not user_data:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
        
        profile = UserProfile(
            id=user_data['id'],
            email=user_data['email'],
            username=user_data['username'],
            plan_type=user_data['plan_type'],
            created_at=user_data['created_at'],
            updated_at=user_data.get('updated_at')
        )
        
        logger.info(f"プロフィール取得完了 - ユーザーID: {current_user['id']}")
        
        return UserProfileResponse(
            profile=profile,
            message="プロフィールを取得しました"
        )
        
    except Exception as e:
        handle_carebot_error(e, "プロフィールの取得に失敗しました")

@router.put("/me", response_model=UserProfileResponse)
async def update_my_profile(
    profile_update: UserProfileUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """現在のユーザーのプロフィールを更新"""
    try:
        logger.info(f"プロフィール更新開始 - ユーザーID: {current_user['id']}")
        
        db = SupabaseDB()
        
        # 更新データを準備
        update_data = {}
        if profile_update.username is not None:
            update_data['username'] = profile_update.username
        if profile_update.email is not None:
            update_data['email'] = profile_update.email
        
        if not update_data:
            raise HTTPException(status_code=400, detail="更新するデータがありません")
        
        # プロフィールを更新
        updated_user = db.update_user(current_user['id'], update_data)
        
        if not updated_user:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
        
        profile = UserProfile(
            id=updated_user['id'],
            email=updated_user['email'],
            username=updated_user['username'],
            plan_type=updated_user['plan_type'],
            created_at=updated_user['created_at'],
            updated_at=updated_user.get('updated_at')
        )
        
        logger.info(f"プロフィール更新完了 - ユーザーID: {current_user['id']}")
        
        return UserProfileResponse(
            profile=profile,
            message="プロフィールを更新しました"
        )
        
    except Exception as e:
        handle_carebot_error(e, "プロフィールの更新に失敗しました")

@router.get("/me/stats", response_model=UserProfileWithStats)
async def get_my_profile_with_stats(current_user: Dict[str, Any] = Depends(get_current_user)):
    """統計情報付きのプロフィールを取得"""
    try:
        logger.info(f"統計付きプロフィール取得開始 - ユーザーID: {current_user['id']}")
        
        db = SupabaseDB()
        
        # ユーザー情報を取得
        user_data = db.get_user_by_id(current_user['id'])
        
        if not user_data:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
        
        # 統計情報を取得
        stats = db.get_user_stats(current_user['id'])
        
        profile = UserProfile(
            id=user_data['id'],
            email=user_data['email'],
            username=user_data['username'],
            plan_type=user_data['plan_type'],
            created_at=user_data['created_at'],
            updated_at=user_data.get('updated_at')
        )
        
        user_stats = UserStats(
            total_journals=stats.get('total_journals', 0),
            total_moods=stats.get('total_moods', 0),
            total_cbt_sessions=stats.get('total_cbt_sessions', 0),
            total_meditation_sessions=stats.get('total_meditation_sessions', 0),
            total_sound_sessions=stats.get('total_sound_sessions', 0),
            total_pomodoro_sessions=stats.get('total_pomodoro_sessions', 0),
            average_mood_score=stats.get('average_mood_score'),
            last_activity=stats.get('last_activity')
        )
        
        logger.info(f"統計付きプロフィール取得完了 - ユーザーID: {current_user['id']}")
        
        return UserProfileWithStats(
            profile=profile,
            stats=user_stats,
            message="統計情報付きプロフィールを取得しました"
        )
        
    except Exception as e:
        handle_carebot_error(e, "統計情報付きプロフィールの取得に失敗しました")

@router.post("/me/change-password", response_model=PasswordChangeResponse)
async def change_password(
    password_change: PasswordChange,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """パスワードを変更"""
    try:
        logger.info(f"パスワード変更開始 - ユーザーID: {current_user['id']}")
        
        db = SupabaseDB()
        
        # 現在のパスワードを確認
        user_data = db.get_user_by_id(current_user['id'])
        
        if not user_data:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
        
        # 現在のパスワードを検証
        if not bcrypt.checkpw(
            password_change.current_password.encode('utf-8'),
            user_data['password_hash'].encode('utf-8')
        ):
            raise HTTPException(status_code=400, detail="現在のパスワードが正しくありません")
        
        # 新しいパスワードをハッシュ化
        new_password_hash = bcrypt.hashpw(
            password_change.new_password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        
        # パスワードを更新
        db.update_user(current_user['id'], {'password_hash': new_password_hash})
        
        logger.info(f"パスワード変更完了 - ユーザーID: {current_user['id']}")
        
        return PasswordChangeResponse(
            message="パスワードを変更しました",
            success=True
        )
        
    except Exception as e:
        handle_carebot_error(e, "パスワードの変更に失敗しました")

@router.delete("/me", response_model=AccountDeleteResponse)
async def delete_my_account(
    account_delete: AccountDelete,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """アカウントを削除"""
    try:
        logger.info(f"アカウント削除開始 - ユーザーID: {current_user['id']}")
        
        db = SupabaseDB()
        
        # ユーザー情報を取得
        user_data = db.get_user_by_id(current_user['id'])
        
        if not user_data:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
        
        # パスワードを確認
        if not bcrypt.checkpw(
            account_delete.password.encode('utf-8'),
            user_data['password_hash'].encode('utf-8')
        ):
            raise HTTPException(status_code=400, detail="パスワードが正しくありません")
        
        # アカウントを削除
        db.delete_user(current_user['id'])
        
        logger.info(f"アカウント削除完了 - ユーザーID: {current_user['id']}")
        
        return AccountDeleteResponse(
            message="アカウントを削除しました",
            success=True
        )
        
    except Exception as e:
        handle_carebot_error(e, "アカウントの削除に失敗しました") 