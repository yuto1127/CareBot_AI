from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class UsageStatus(BaseModel):
    """使用状況スキーマ"""
    user_id: int
    feature_type: str
    current_usage: int
    limit: int
    remaining: int
    percentage: float
    reset_date: str

class UsageResponse(BaseModel):
    """使用回数レスポンススキーマ"""
    usage: Dict[str, UsageStatus]
    plan_type: str
    plan_limits: Dict[str, int]

class UsageIncrement(BaseModel):
    """使用回数増加スキーマ"""
    feature_type: str
    amount: int = Field(default=1, ge=1, description="増加量")

class UsageLimit(BaseModel):
    """使用制限スキーマ"""
    feature_type: str
    limit: int = Field(..., ge=1, description="制限回数")
    reset_period: str = Field(default="monthly", description="リセット期間") 