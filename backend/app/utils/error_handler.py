from fastapi import HTTPException, Request
from typing import Dict, Any, Optional
from .logger import logger

class CareBotError(Exception):
    """CareBot AI カスタムエラーベースクラス"""
    
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

class AuthenticationError(CareBotError):
    """認証エラー"""
    def __init__(self, message: str = "認証に失敗しました", details: Dict[str, Any] = None):
        super().__init__(message, "AUTH_ERROR", details)

class AuthorizationError(CareBotError):
    """認可エラー"""
    def __init__(self, message: str = "アクセス権限がありません", details: Dict[str, Any] = None):
        super().__init__(message, "AUTHZ_ERROR", details)

class ValidationError(CareBotError):
    """バリデーションエラー"""
    def __init__(self, message: str = "入力データが無効です", details: Dict[str, Any] = None):
        super().__init__(message, "VALIDATION_ERROR", details)

class DatabaseError(CareBotError):
    """データベースエラー"""
    def __init__(self, message: str = "データベースエラーが発生しました", details: Dict[str, Any] = None):
        super().__init__(message, "DB_ERROR", details)

class UsageLimitError(CareBotError):
    """使用制限エラー"""
    def __init__(self, message: str = "使用回数制限に達しました", details: Dict[str, Any] = None):
        super().__init__(message, "USAGE_LIMIT_ERROR", details)

class ResourceNotFoundError(CareBotError):
    """リソース未発見エラー"""
    def __init__(self, message: str = "リソースが見つかりません", details: Dict[str, Any] = None):
        super().__init__(message, "NOT_FOUND_ERROR", details)

class ExternalServiceError(CareBotError):
    """外部サービスエラー"""
    def __init__(self, message: str = "外部サービスでエラーが発生しました", details: Dict[str, Any] = None):
        super().__init__(message, "EXTERNAL_SERVICE_ERROR", details)

def handle_carebot_error(error: CareBotError, request: Request) -> HTTPException:
    """CareBotエラーをHTTPExceptionに変換"""
    # エラーログを記録
    logger.log_api_error(
        method=request.method,
        path=str(request.url.path),
        error=error,
        user_id=getattr(request.state, 'user_id', None)
    )
    
    # エラーコードに基づいてHTTPステータスコードを決定
    status_code_map = {
        "AUTH_ERROR": 401,
        "AUTHZ_ERROR": 403,
        "VALIDATION_ERROR": 400,
        "DB_ERROR": 500,
        "USAGE_LIMIT_ERROR": 429,
        "NOT_FOUND_ERROR": 404,
        "EXTERNAL_SERVICE_ERROR": 502
    }
    
    status_code = status_code_map.get(error.error_code, 500)
    
    return HTTPException(
        status_code=status_code,
        detail={
            "error": error.message,
            "error_code": error.error_code,
            "details": error.details
        }
    )

def handle_general_error(error: Exception, request: Request) -> HTTPException:
    """一般的なエラーをハンドリング"""
    # エラーログを記録
    logger.log_api_error(
        method=request.method,
        path=str(request.url.path),
        error=error,
        user_id=getattr(request.state, 'user_id', None)
    )
    
    # エラータイプに基づいてメッセージを決定
    error_messages = {
        "ValueError": "無効な値が入力されました",
        "TypeError": "データ型エラーが発生しました",
        "KeyError": "必要なデータが見つかりません",
        "IndexError": "配列インデックスエラーが発生しました",
        "AttributeError": "オブジェクト属性エラーが発生しました",
        "ImportError": "モジュール読み込みエラーが発生しました",
        "ConnectionError": "接続エラーが発生しました",
        "TimeoutError": "タイムアウトエラーが発生しました"
    }
    
    error_type = type(error).__name__
    message = error_messages.get(error_type, "予期しないエラーが発生しました")
    
    return HTTPException(
        status_code=500,
        detail={
            "error": message,
            "error_code": "INTERNAL_ERROR",
            "details": {
                "original_error": str(error),
                "error_type": error_type
            }
        }
    )

def create_error_response(error: Exception, request: Request) -> HTTPException:
    """エラーレスポンスを作成"""
    if isinstance(error, CareBotError):
        return handle_carebot_error(error, request)
    else:
        return handle_general_error(error, request)

def log_request_info(request: Request, user_id: Optional[int] = None):
    """リクエスト情報をログに記録"""
    logger.log_api_request(
        method=request.method,
        path=str(request.url.path),
        user_id=user_id
    )

def validate_required_fields(data: Dict[str, Any], required_fields: list) -> None:
    """必須フィールドのバリデーション"""
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            missing_fields.append(field)
    
    if missing_fields:
        raise ValidationError(
            f"必須フィールドが不足しています: {', '.join(missing_fields)}",
            {"missing_fields": missing_fields}
        )

def validate_data_types(data: Dict[str, Any], field_types: Dict[str, type]) -> None:
    """データ型のバリデーション"""
    type_errors = []
    for field, expected_type in field_types.items():
        if field in data and not isinstance(data[field], expected_type):
            type_errors.append(f"{field}: 期待される型 {expected_type.__name__}, 実際の型 {type(data[field]).__name__}")
    
    if type_errors:
        raise ValidationError(
            f"データ型エラー: {'; '.join(type_errors)}",
            {"type_errors": type_errors}
        )

def sanitize_error_message(message: str) -> str:
    """エラーメッセージをサニタイズ（機密情報を除去）"""
    # 機密情報を除去
    sensitive_patterns = [
        r'password["\']?\s*[:=]\s*["\'][^"\']*["\']',
        r'token["\']?\s*[:=]\s*["\'][^"\']*["\']',
        r'secret["\']?\s*[:=]\s*["\'][^"\']*["\']',
        r'key["\']?\s*[:=]\s*["\'][^"\']*["\']'
    ]
    
    import re
    sanitized_message = message
    for pattern in sensitive_patterns:
        sanitized_message = re.sub(pattern, r'\1: [REDACTED]', sanitized_message)
    
    return sanitized_message 