import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# ログ設定
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# ログフォーマット
if ENVIRONMENT == "production":
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
else:
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"

# ログ設定
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f"logs/app_{datetime.now().strftime('%Y%m%d')}.log")
    ]
)

logger = logging.getLogger("carebot")

class CareBotLogger:
    """CareBot AI 専用ロガークラス"""
    
    def __init__(self):
        self.logger = logger
    
    def info(self, message: str, error: Optional[Exception] = None, context: Optional[Dict[str, Any]] = None):
        """情報ログ"""
        log_message = f"{message}"
        if context:
            log_message += f" | Context: {context}"
        if error:
            log_message += f" | Error: {str(error)}"
        self.logger.info(log_message)
    
    def warning(self, message: str, error: Optional[Exception] = None, context: Optional[Dict[str, Any]] = None):
        """警告ログ"""
        log_message = f"{message}"
        if context:
            log_message += f" | Context: {context}"
        if error:
            log_message += f" | Error: {str(error)}"
        self.logger.warning(log_message)
    
    def error(self, message: str, error: Optional[Exception] = None, context: Optional[Dict[str, Any]] = None):
        """エラーログ"""
        log_message = f"{message}"
        if context:
            log_message += f" | Context: {context}"
        if error:
            log_message += f" | Error: {str(error)}"
        self.logger.error(log_message, exc_info=error is not None)
    
    def debug(self, message: str, context: Optional[Dict[str, Any]] = None):
        """デバッグログ"""
        log_message = f"{message}"
        if context:
            log_message += f" | Context: {context}"
        self.logger.debug(log_message)
    
    def log_api_request(self, method: str, path: str, user_id: Optional[int] = None):
        """APIリクエストログ"""
        context = {"method": method, "path": path}
        if user_id:
            context["user_id"] = user_id
        self.info("API Request", context=context)
    
    def log_api_error(self, method: str, path: str, error: Exception, user_id: Optional[int] = None):
        """APIエラーログ"""
        context = {"method": method, "path": path}
        if user_id:
            context["user_id"] = user_id
        self.error("API Error", error=error, context=context)
    
    def log_user_action(self, user_id: int, action: str, details: Optional[Dict[str, Any]] = None):
        """ユーザーアクションログ"""
        context = {"user_id": user_id, "action": action}
        if details:
            context.update(details)
        self.info("User Action", context=context)
    
    def log_security_event(self, event_type: str, user_id: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        """セキュリティイベントログ"""
        context = {"event_type": event_type}
        if user_id:
            context["user_id"] = user_id
        if details:
            context.update(details)
        self.warning("Security Event", context=context)

# グローバルロガーインスタンス
logger = CareBotLogger() 