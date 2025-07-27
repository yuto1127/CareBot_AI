from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional
from app.utils.auth import get_current_user
from app.utils.cbt_analyzer import CBTAnalyzer
from app.utils.usage_limits import can_use_feature, increment_usage
from app.database.supabase_db import SupabaseDB
import json

router = APIRouter(prefix="/cbt", tags=["CBT"])

# CBTアナライザーの初期化（完全無料版）
cbt_analyzer = CBTAnalyzer()

@router.post("/session/start")
def start_cbt_session(
    initial_thought: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """CBTセッションを開始"""
    # 使用制限チェック
    if not can_use_feature(current_user['id'], 'cbt_session'):
        raise HTTPException(
            status_code=429,
            detail="CBTセッションの使用回数上限に達しました。プレミアムプランへのアップグレードをご検討ください。"
        )
    
    try:
        # セッション開始
        session_data = cbt_analyzer.start_cbt_session(
            user_id=current_user['id'],
            initial_thought=initial_thought
        )
        
        # 使用回数を増加
        increment_usage(current_user['id'], 'cbt_session')
        
        return {
            "session_id": session_data["session_id"],
            "message": session_data["conversation"][0]["content"],
            "session_data": session_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CBTセッション開始エラー: {str(e)}")

@router.post("/session/{session_id}/continue")
def continue_cbt_session(
    session_id: str,
    message: str,
    current_user: dict = Depends(get_current_user)
):
    """CBTセッションを継続"""
    try:
        # セッションデータを取得（実際の実装ではデータベースから取得）
        # ここでは簡易実装
        session_data = {
            "session_id": session_id,
            "user_id": current_user['id'],
            "conversation": []
        }
        
        # 危機的状況を検知
        if cbt_analyzer.detect_crisis(message):
            return {
                "session_id": session_id,
                "message": cbt_analyzer.get_crisis_response(),
                "crisis_detected": True,
                "session_data": session_data
            }
        
        # セッション継続
        updated_session = cbt_analyzer.continue_cbt_session(session_data, message)
        
        return {
            "session_id": session_id,
            "message": updated_session["conversation"][-1]["content"],
            "session_data": updated_session
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CBTセッション継続エラー: {str(e)}")

@router.post("/session/{session_id}/end")
def end_cbt_session(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """CBTセッションを終了"""
    try:
        # セッションデータを取得（実際の実装ではデータベースから取得）
        session_data = {
            "session_id": session_id,
            "user_id": current_user['id'],
            "conversation": []
        }
        
        # セッション終了
        completed_session = cbt_analyzer.end_cbt_session(session_data)
        
        return {
            "session_id": session_id,
            "summary": completed_session.get("summary", ""),
            "message": "CBTセッションが完了しました。セッション内容はジャーナルに保存されました。",
            "session_data": completed_session
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CBTセッション終了エラー: {str(e)}")

@router.get("/sessions")
def get_cbt_sessions(current_user: dict = Depends(get_current_user)):
    """ユーザーのCBTセッション履歴を取得"""
    try:
        # CBTセッションをジャーナルから取得
        journals = SupabaseDB.get_user_journals(current_user['id'])
        cbt_sessions = [
            journal for journal in journals 
            if journal.get('session_type') == 'cbt'
        ]
        
        return {
            "sessions": cbt_sessions,
            "total_count": len(cbt_sessions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CBTセッション履歴取得エラー: {str(e)}")

@router.get("/session/{session_id}")
def get_cbt_session(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """特定のCBTセッション詳細を取得"""
    try:
        # セッションIDでジャーナルを検索
        journals = SupabaseDB.get_user_journals(current_user['id'])
        session_journal = None
        
        for journal in journals:
            if journal.get('session_id') == session_id:
                session_journal = journal
                break
        
        if not session_journal:
            raise HTTPException(status_code=404, detail="CBTセッションが見つかりません")
        
        return {
            "session": session_journal
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CBTセッション取得エラー: {str(e)}") 