"""
CBT対話用のPydanticスキーマ
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class CBTRequest(BaseModel):
    """CBT対話リクエストスキーマ"""
    message: str = Field(..., min_length=1, max_length=1000, description="ユーザーのメッセージ")
    session_id: Optional[str] = Field(None, description="セッションID")
    context: Optional[Dict[str, Any]] = Field(None, description="対話コンテキスト")

class CBTResponse(BaseModel):
    """CBT対話レスポンススキーマ"""
    message: str = Field(..., description="AIの応答メッセージ")
    emotion: str = Field(..., description="検出された感情")
    crisis_detected: bool = Field(..., description="危機的状況の検出フラグ")
    session_id: Optional[str] = Field(None, description="セッションID")
    timestamp: str = Field(..., description="応答タイムスタンプ")
    context: Optional[Dict[str, Any]] = Field(None, description="更新されたコンテキスト")

class CBTSessionRequest(BaseModel):
    """CBTセッション開始リクエストスキーマ"""
    initial_message: Optional[str] = Field(None, max_length=1000, description="初期メッセージ")

class CBTSessionResponse(BaseModel):
    """CBTセッション開始レスポンススキーマ"""
    session_id: str = Field(..., description="セッションID")
    welcome_message: str = Field(..., description="歓迎メッセージ")
    timestamp: str = Field(..., description="セッション開始タイムスタンプ")

class CBTConversationHistory(BaseModel):
    """CBT対話履歴スキーマ"""
    session_id: str = Field(..., description="セッションID")
    conversations: list = Field(..., description="対話履歴")
    summary: str = Field(..., description="対話要約")
    created_at: str = Field(..., description="作成日時")
    updated_at: str = Field(..., description="更新日時")

class CBTQualityReport(BaseModel):
    """CBT品質レポートスキーマ"""
    total_conversations: int = Field(..., description="総対話数")
    crisis_detection_rate: float = Field(..., description="危機検出率")
    average_response_length: float = Field(..., description="平均応答長")
    emotion_distribution: Dict[str, int] = Field(..., description="感情分布")
    timestamp: str = Field(..., description="レポート生成タイムスタンプ") 