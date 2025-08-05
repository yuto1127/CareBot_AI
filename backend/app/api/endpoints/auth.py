from fastapi import APIRouter, HTTPException, Request, Depends
from typing import Dict, Any
from datetime import datetime
from app.schemas.auth import UserLogin, UserResponse
from app.schemas.user import UserCreate
from app.schemas.legal import LegalAgreement, LegalAgreementResponse
from app.database.supabase_db import SupabaseDB
from app.utils.auth import create_access_token, get_current_user
from app.utils.logger import logger
from app.utils.error_handler import (
    AuthenticationError, ValidationError, DatabaseError,
    create_error_response, log_request_info, validate_required_fields
)
import re

router = APIRouter(tags=["auth"])

def validate_email(email: str) -> bool:
    """メールアドレスの形式を検証"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> bool:
    """パスワードの強度を検証"""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, request: Request):
    """ユーザー登録"""
    try:
        # リクエストログ
        log_request_info(request)
        logger.info(f"=== ユーザー登録開始 ===")
        logger.info(f"登録メールアドレス: {user_data.email}")
        logger.info(f"登録ユーザー名: {user_data.name}")
        
        # バリデーション
        validate_required_fields(user_data.dict(), ['email', 'password', 'name'])
        
        # メールアドレスの形式検証
        if not validate_email(user_data.email):
            logger.warning(f"無効なメールアドレス形式: {user_data.email}")
            raise ValidationError("無効なメールアドレス形式です")
        
        # パスワードの強度検証
        if not validate_password(user_data.password):
            logger.warning(f"パスワード強度不足: {user_data.email}")
            raise ValidationError("パスワードは8文字以上で、大文字・小文字・数字を含む必要があります")
        
        # ユーザー名の検証
        if len(user_data.name) < 2 or len(user_data.name) > 50:
            logger.warning(f"ユーザー名長エラー: {user_data.name}")
            raise ValidationError("ユーザー名は2文字以上50文字以下である必要があります")
        
        # 既存ユーザーの確認
        existing_user = SupabaseDB.get_user_by_email(user_data.email)
        if existing_user:
            logger.warning(f"既存ユーザー登録試行: {user_data.email}")
            raise ValidationError("このメールアドレスは既に登録されています")
        
        # ユーザー登録処理
        logger.info(f"データベースにユーザー登録中: {user_data.email}")
        user = SupabaseDB.create_user(user_data)
        if not user:
            logger.error(f"ユーザー登録失敗: {user_data.email}")
            raise DatabaseError("ユーザー登録に失敗しました")
        
        # アクセストークン生成
        access_token = create_access_token(data={"sub": str(user['id'])})
        logger.info(f"アクセストークン生成完了: ユーザーID {user['id']}")
        
        # 成功ログ
        logger.log_user_action(
            user_id=user['id'],
            action="user_registration",
            details={"email": user_data.email, "name": user_data.name}
        )
        
        logger.info(f"=== ユーザー登録完了 ===")
        logger.info(f"登録成功: {user_data.email} (ID: {user['id']})")
        
        return {
            "user": user,
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except ValidationError as e:
        logger.error(f"登録バリデーションエラー: {e.message}")
        raise create_error_response(e, request)
    except DatabaseError as e:
        logger.error(f"登録データベースエラー: {e.message}")
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
        logger.info(f"=== ユーザーログイン開始 ===")
        logger.info(f"ログインメールアドレス: {user_data.email}")
        
        # バリデーション
        validate_required_fields(user_data.dict(), ['email', 'password'])
        
        # メールアドレスの形式検証
        if not validate_email(user_data.email):
            logger.warning(f"無効なメールアドレス形式: {user_data.email}")
            raise ValidationError("無効なメールアドレス形式です")
        
        # ログイン処理
        logger.info(f"認証処理開始: {user_data.email}")
        user = SupabaseDB.authenticate_user(user_data.email, user_data.password)
        
        if not user:
            logger.warning(f"認証失敗: {user_data.email}")
            raise AuthenticationError("メールアドレスまたはパスワードが正しくありません")
        
        # アクセストークン生成
        access_token = create_access_token(data={"sub": str(user['id'])})
        logger.info(f"アクセストークン生成完了: ユーザーID {user['id']}")
        
        # 成功ログ
        logger.log_user_action(
            user_id=user['id'],
            action="user_login",
            details={"email": user_data.email}
        )
        
        logger.info(f"=== ユーザーログイン完了 ===")
        logger.info(f"ログイン成功: {user_data.email} (ID: {user['id']})")
        
        return {
            "user": user,
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except AuthenticationError as e:
        logger.error(f"ログイン認証エラー: {e.message}")
        raise create_error_response(e, request)
    except ValidationError as e:
        logger.error(f"ログインバリデーションエラー: {e.message}")
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

@router.get("/me")
async def get_current_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    """現在のユーザー情報を取得"""
    try:
        return {
            "user": current_user
        }
    except Exception as e:
        logger.error("ユーザー情報取得エラー", e)
        raise HTTPException(status_code=500, detail="ユーザー情報の取得に失敗しました")

@router.post("/legal-agreement", response_model=LegalAgreementResponse)
async def record_legal_agreement(agreement: LegalAgreement, request: Request):
    """法的・倫理的ポジショニングの同意確認を記録"""
    try:
        # リクエストログ
        log_request_info(request)
        logger.info(f"=== 法的・倫理的ポジショニング同意確認 ===")
        
        # バリデーション
        if not agreement.privacy_policy_agreed:
            raise ValidationError("プライバシーポリシーへの同意が必要です")
        if not agreement.terms_of_service_agreed:
            raise ValidationError("利用規約への同意が必要です")
        if not agreement.safety_guidelines_agreed:
            raise ValidationError("セーフティガード機能への同意が必要です")
        
        # 同意日時を設定
        if not agreement.agreement_date:
            agreement.agreement_date = datetime.utcnow()
        
        # IPアドレスとユーザーエージェントを記録
        agreement.ip_address = request.client.host if request.client else None
        agreement.user_agent = request.headers.get("user-agent")
        
        # 同意記録をデータベースに保存（オプション）
        # ここではログに記録するのみ
        logger.info(f"法的・倫理的ポジショニング同意確認記録:")
        logger.info(f"  同意日時: {agreement.agreement_date}")
        logger.info(f"  IPアドレス: {agreement.ip_address}")
        logger.info(f"  ユーザーエージェント: {agreement.user_agent}")
        
        logger.info(f"=== 法的・倫理的ポジショニング同意確認完了 ===")
        
        return {
            "message": "法的・倫理的ポジショニングへの同意が記録されました",
            "agreement_id": f"legal_{int(agreement.agreement_date.timestamp())}",
            "agreement_date": agreement.agreement_date
        }
        
    except ValidationError as e:
        logger.error(f"法的・倫理的ポジショニング同意確認エラー: {e.message}")
        raise create_error_response(e, request)
    except Exception as e:
        logger.error("法的・倫理的ポジショニング同意確認エラー", e)
        raise create_error_response(e, request) 