import logging
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import json

class Logger:
    """アプリケーションログ管理クラス"""
    
    def __init__(self, name: str = "carebot_ai"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # ログディレクトリの作成
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # ファイルハンドラーの設定
        file_handler = logging.FileHandler(
            f"{log_dir}/app_{datetime.now().strftime('%Y%m%d')}.log",
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        
        # コンソールハンドラーの設定
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # フォーマッターの設定
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # ハンドラーの追加
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """情報ログ"""
        if extra:
            message = f"{message} - {self._safe_json_dumps(extra)}"
        self.logger.info(message)
    
    def error(self, message: str, error: Optional[Exception] = None, extra: Optional[Dict[str, Any]] = None):
        """エラーログ"""
        if error:
            message = f"{message} - Error: {str(error)}"
        if extra:
            message = f"{message} - {self._safe_json_dumps(extra)}"
        self.logger.error(message)
    
    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """警告ログ"""
        if extra:
            message = f"{message} - {self._safe_json_dumps(extra)}"
        self.logger.warning(message)
    
    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """デバッグログ"""
        if extra:
            message = f"{message} - {self._safe_json_dumps(extra)}"
        self.logger.debug(message)
    
    def _safe_json_dumps(self, obj: Any) -> str:
        """安全なJSONシリアライズ"""
        try:
            return json.dumps(obj, ensure_ascii=False, default=str)
        except Exception as e:
            return f"JSON serialization error: {str(e)} - Object: {str(obj)}"
    
    def log_api_request(self, method: str, path: str, user_id: Optional[int] = None, status_code: int = 200):
        """APIリクエストログ"""
        extra = {
            "method": method,
            "path": path,
            "user_id": user_id,
            "status_code": status_code,
            "timestamp": datetime.now().isoformat()
        }
        self.info(f"API Request: {method} {path}", extra)
    
    def log_api_error(self, method: str, path: str, error: Exception, user_id: Optional[int] = None):
        """APIエラーログ"""
        extra = {
            "method": method,
            "path": path,
            "user_id": user_id,
            "error_type": type(error).__name__,
            "timestamp": datetime.now().isoformat()
        }
        self.error(f"API Error: {method} {path}", error, extra)
    
    def log_user_action(self, user_id: int, action: str, details: Optional[Dict[str, Any]] = None):
        """ユーザーアクションログ"""
        extra = {
            "user_id": user_id,
            "action": action,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.info(f"User Action: {action}", extra)
    
    def log_database_operation(self, operation: str, table: str, user_id: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        """データベース操作ログ"""
        extra = {
            "operation": operation,
            "table": table,
            "user_id": user_id,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.info(f"Database Operation: {operation} on {table}", extra)

# グローバルロガーインスタンス
logger = Logger() 