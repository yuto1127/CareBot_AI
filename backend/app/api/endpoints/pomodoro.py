from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any, Optional
from app.utils.auth import get_current_user
from app.utils.pomodoro_timer import PomodoroTimer
from app.utils.usage_limits import can_use_feature, increment_usage
from app.database.supabase_db import SupabaseDB

router = APIRouter(prefix="/pomodoro", tags=["Pomodoro"])

# ポモドーロタイマーの初期化
pomodoro_timer = PomodoroTimer()

@router.post("/session/create")
def create_pomodoro_session(
    settings: Optional[Dict[str, Any]] = None,
    current_user: dict = Depends(get_current_user)
):
    """ポモドーロセッションを作成"""
    try:
        session_data = pomodoro_timer.create_session(current_user['id'], settings)
        
        return {
            "message": "ポモドーロセッションを作成しました",
            "session_data": session_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"セッション作成エラー: {str(e)}")

@router.post("/session/start-focus")
def start_focus_session(
    session_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """集中セッションを開始"""
    # 使用制限チェック
    if not can_use_feature(current_user['id'], 'pomodoro_session'):
        raise HTTPException(
            status_code=429,
            detail="ポモドーロセッションの使用回数上限に達しました。プレミアムプランへのアップグレードをご検討ください。"
        )
    
    try:
        updated_session = pomodoro_timer.start_focus_session(session_data)
        
        # 使用回数を増加
        increment_usage(current_user['id'], 'pomodoro_session')
        
        return {
            "message": "集中セッションを開始しました",
            "session_data": updated_session
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"集中セッション開始エラー: {str(e)}")

@router.post("/session/start-break")
def start_break_session(
    session_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """休憩セッションを開始"""
    try:
        updated_session = pomodoro_timer.start_break_session(session_data)
        
        return {
            "message": "休憩セッションを開始しました",
            "session_data": updated_session
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"休憩セッション開始エラー: {str(e)}")

@router.post("/session/pause")
def pause_session(
    session_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """セッションを一時停止"""
    try:
        updated_session = pomodoro_timer.pause_session(session_data)
        
        return {
            "message": "セッションを一時停止しました",
            "session_data": updated_session
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"セッション一時停止エラー: {str(e)}")

@router.post("/session/resume")
def resume_session(
    session_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """セッションを再開"""
    try:
        updated_session = pomodoro_timer.resume_session(session_data)
        
        return {
            "message": "セッションを再開しました",
            "session_data": updated_session
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"セッション再開エラー: {str(e)}")

@router.post("/session/complete")
def complete_session(
    session_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """セッションを完了"""
    try:
        completed_session = pomodoro_timer.complete_session(session_data)
        
        return {
            "message": "ポモドーロセッションを完了しました",
            "session_data": completed_session
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"セッション完了エラー: {str(e)}")

@router.post("/session/progress")
def get_session_progress(
    session_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """セッションの進行状況を取得"""
    try:
        progress = pomodoro_timer.get_session_progress(session_data)
        
        return {
            "progress": progress,
            "session_data": session_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"進行状況取得エラー: {str(e)}")

@router.get("/statistics")
def get_user_statistics(current_user: dict = Depends(get_current_user)):
    """ユーザーのポモドーロ統計を取得"""
    try:
        statistics = pomodoro_timer.get_user_statistics(current_user['id'])
        
        return {
            "statistics": statistics
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"統計取得エラー: {str(e)}")

@router.get("/history")
def get_pomodoro_history(current_user: dict = Depends(get_current_user)):
    """ポモドーロ履歴を取得"""
    try:
        # ポモドーロセッションをジャーナルから取得
        journals = SupabaseDB.get_user_journals(current_user['id'])
        pomodoro_sessions = [
            journal for journal in journals 
            if journal.get('session_type') == 'pomodoro'
        ]
        
        return {
            "sessions": pomodoro_sessions,
            "total_count": len(pomodoro_sessions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"履歴取得エラー: {str(e)}")

@router.get("/settings/default")
def get_default_settings():
    """デフォルト設定を取得"""
    try:
        return {
            "settings": pomodoro_timer.default_settings
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"設定取得エラー: {str(e)}")

@router.get("/states")
def get_session_states():
    """セッション状態一覧を取得"""
    try:
        return {
            "states": pomodoro_timer.session_states
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"状態取得エラー: {str(e)}") 