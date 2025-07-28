from fastapi import APIRouter, HTTPException, Request, Depends
from typing import Dict, Any
from app.schemas.auth import UserRegister, UserLogin, UserResponse
from app.database.supabase_db import SupabaseDB
from app.utils.auth import create_access_token, get_current_user
from app.utils.logger import logger
from app.utils.error_handler import (
    AuthenticationError, ValidationError, DatabaseError,
    create_error_response, log_request_info, validate_required_fields
)

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserRegister, request: Request):
    """ユーザー登録"""
    try:
        # リクエストログ
        log_request_info(request)
        
        # バリデーション
        validate_required_fields(user_data.dict(), ['email', 'password', 'username'])
        
        # ユーザー登録処理
        user = SupabaseDB.create_user(user_data.dict())
        
        # アクセストークン生成
        access_token = create_access_token(data={"sub": str(user['id'])})
        
        # 成功ログ
        logger.log_user_action(
            user_id=user['id'],
            action="user_registration",
            details={"email": user_data.email, "username": user_data.username}
        )
        
        return {
            "user": user,
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except ValidationError as e:
        raise create_error_response(e, request)
    except DatabaseError as e:
        raise create_error_response(e, request)
    except Exception as e:
        logger.error("ユーザー登録エラー", e, {"email": user_data.email})
        raise create_error_response(e, request)

@router.post("/login", response_model=UserResponse)
async def login(user_data: UserLogin, request: Request):
    """ユーザーログイン"""
    try:
        # リクエストログ
        log_request_info(request)
        
        # バリデーション
        validate_required_fields(user_data.dict(), ['email', 'password'])
        
        # ログイン処理
        user = SupabaseDB.authenticate_user(user_data.email, user_data.password)
        
        if not user:
            raise AuthenticationError("メールアドレスまたはパスワードが正しくありません")
        
        # アクセストークン生成
        access_token = create_access_token(data={"sub": str(user['id'])})
        
        # 成功ログ
        logger.log_user_action(
            user_id=user['id'],
            action="user_login",
            details={"email": user_data.email}
        )
        
        return {
            "user": user,
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except AuthenticationError as e:
        raise create_error_response(e, request)
    except ValidationError as e:
        raise create_error_response(e, request)
    except Exception as e:
        logger.error("ログインエラー", e, {"email": user_data.email})
        raise create_error_response(e, request)

@router.post("/logout")
async def logout(current_user: Dict[str, Any] = Depends(get_current_user), request: Request = None):
    """ユーザーログアウト"""
    try:
        # リクエストログ
        if request:
            log_request_info(request, current_user['id'])
        
        # ログアウトログ
        logger.log_user_action(
            user_id=current_user['id'],
            action="user_logout"
        )
        
        return {"message": "ログアウトしました"}
        
    except Exception as e:
        if request:
            raise create_error_response(e, request)
        else:
            raise HTTPException(status_code=500, detail="ログアウトエラー") 