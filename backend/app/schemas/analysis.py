from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List

class AnalysisRequest(BaseModel):
    """分析リクエストスキーマ"""
    analysis_type: str = Field(..., description="分析タイプ")
    parameters: Optional[Dict[str, Any]] = Field(default={}, description="分析パラメータ")

class AnalysisResponse(BaseModel):
    """分析レスポンススキーマ"""
    id: int
    user_id: int
    analysis_type: str
    result: Dict[str, Any]
    insights: List[str]
    created_at: str

class AnalysisListResponse(BaseModel):
    """分析一覧レスポンススキーマ"""
    analyses: List[AnalysisResponse]
    total_count: int

class StressAnalysis(BaseModel):
    """ストレス分析スキーマ"""
    stress_level: str = Field(..., description="ストレスレベル")
    factors: List[str] = Field(default=[], description="ストレス要因")
    recommendations: List[str] = Field(default=[], description="推奨事項")

class MoodTrendAnalysis(BaseModel):
    """気分傾向分析スキーマ"""
    trend: str = Field(..., description="気分傾向")
    average_mood: float = Field(..., description="平均気分")
    mood_patterns: List[Dict[str, Any]] = Field(default=[], description="気分パターン") 