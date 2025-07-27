import json
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.utils.auth import get_current_user
from app.utils.usage_limits import can_use_feature, increment_usage
from app.utils.ai_analyzer import AIAnalyzer
from app.database.supabase_db import SupabaseDB

router = APIRouter()

@router.get("/", response_model=List[AnalysisResponse])
def get_analyses(current_user: dict = Depends(get_current_user)):
    """ユーザーの分析結果一覧を取得"""
    analyses = SupabaseDB.get_user_analyses(current_user['id'])
    
    # JSON文字列をリストに変換
    for analysis in analyses:
        if isinstance(analysis.get('insights'), str):
            try:
                analysis['insights'] = json.loads(analysis['insights'])
            except:
                analysis['insights'] = []
        
        if isinstance(analysis.get('recommendations'), str):
            try:
                analysis['recommendations'] = json.loads(analysis['recommendations'])
            except:
                analysis['recommendations'] = []
    
    return analyses

@router.post("/", response_model=AnalysisResponse)
def create_analysis(
    analysis_request: AnalysisRequest,
    current_user: dict = Depends(get_current_user)
):
    """AI分析を実行"""
    # 使用回数制限をチェック
    usage_check = can_use_feature(current_user['id'], "ai_analysis")
    if not usage_check["can_use"]:
        raise HTTPException(
            status_code=429,
            detail={
                "message": "使用回数制限に達しました",
                "current_usage": usage_check["current_usage"],
                "limit": usage_check["limit"],
                "plan_type": usage_check["plan_type"],
                "upgrade_required": True
            }
        )
    
    # AI分析を実行
    analyzer = AIAnalyzer()
    analysis_result = analyzer.analyze_combined(
        analysis_request.journal_ids,
        analysis_request.mood_ids,
        analysis_request.analysis_type
    )
    
    # 分析結果を保存
    db_analysis = SupabaseDB.create_analysis(current_user['id'], analysis_result)
    if not db_analysis:
        raise HTTPException(
            status_code=500,
            detail="Failed to save analysis result"
        )
    
    # 使用回数を増加
    increment_usage(current_user['id'], "ai_analysis")
    
    # JSON文字列をリストに変換してから返す
    if isinstance(db_analysis.get('insights'), str):
        try:
            db_analysis['insights'] = json.loads(db_analysis['insights'])
        except:
            db_analysis['insights'] = []
    
    if isinstance(db_analysis.get('recommendations'), str):
        try:
            db_analysis['recommendations'] = json.loads(db_analysis['recommendations'])
        except:
            db_analysis['recommendations'] = []
    
    return db_analysis

@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: int,
    current_user: dict = Depends(get_current_user)
):
    """特定の分析結果を取得"""
    analyses = SupabaseDB.get_user_analyses(current_user['id'])
    analysis = next((a for a in analyses if a['id'] == analysis_id), None)
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # JSON文字列をリストに変換してから返す
    if isinstance(analysis.get('insights'), str):
        try:
            analysis['insights'] = json.loads(analysis['insights'])
        except:
            analysis['insights'] = []
    
    if isinstance(analysis.get('recommendations'), str):
        try:
            analysis['recommendations'] = json.loads(analysis['recommendations'])
        except:
            analysis['recommendations'] = []
    
    return analysis

@router.delete("/{analysis_id}")
def delete_analysis(
    analysis_id: int,
    current_user: dict = Depends(get_current_user)
):
    """分析結果を削除"""
    # 実装は後で追加
    return {"message": "Analysis deleted"} 