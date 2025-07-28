from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any, Optional
from app.utils.auth import get_current_user
from app.utils.meditation_guide import MeditationGuide
from app.utils.usage_limits import can_use_feature, increment_usage
from app.database.supabase_db import SupabaseDB

router = APIRouter(tags=["meditation"])

# 瞑想ガイドの初期化
meditation_guide = MeditationGuide()

@router.get("/sessions")
def get_meditation_sessions(
    category: Optional[str] = None,
    max_duration: Optional[int] = None,
    current_user: dict = Depends(get_current_user)
):
    """瞑想セッション一覧を取得"""
    try:
        if category:
            sessions = meditation_guide.get_sessions_by_category(category)
        elif max_duration:
            sessions = meditation_guide.get_sessions_by_duration(max_duration)
        else:
            sessions = meditation_guide.get_all_sessions()
        
        return {
            "sessions": sessions,
            "total_count": len(sessions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"瞑想セッション取得エラー: {str(e)}")

@router.get("/sessions/{session_id}")
def get_meditation_session(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """特定の瞑想セッション詳細を取得"""
    try:
        session = meditation_guide.get_session_by_id(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="瞑想セッションが見つかりません")
        
        return {"session": session}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"瞑想セッション取得エラー: {str(e)}")

@router.get("/meditation-recommendations")
def get_personalized_recommendations(
    context: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """パーソナライズされた推奨セッションを取得"""
    try:
        recommendations = meditation_guide.get_personalized_recommendations(
            current_user['id'], 
            context
        )
        
        return {
            "recommendations": recommendations,
            "context": context
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推奨取得エラー: {str(e)}")

@router.post("/sessions/{session_id}/start")
def start_meditation_session(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """瞑想セッションを開始"""
    # 使用制限チェック
    if not can_use_feature(current_user['id'], 'meditation_session'):
        raise HTTPException(
            status_code=429,
            detail="瞑想セッションの使用回数上限に達しました。プレミアムプランへのアップグレードをご検討ください。"
        )
    
    try:
        session_data = meditation_guide.start_meditation_session(
            current_user['id'], 
            session_id
        )
        
        # 使用回数を増加
        increment_usage(current_user['id'], 'meditation_session')
        
        return {
            "message": "瞑想セッションを開始しました",
            "session_data": session_data
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"セッション開始エラー: {str(e)}")

@router.post("/sessions/{session_id}/complete")
def complete_meditation_session(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """瞑想セッションを完了"""
    try:
        # セッションデータを取得（実際の実装ではデータベースから取得）
        session_data = {
            "session_id": session_id,
            "user_id": current_user['id'],
            "start_time": "2024-01-01T00:00:00",  # 実際の実装では保存されたデータを使用
            "duration": 300,
            "title": "瞑想セッション",
            "audio_url": "/audio/meditation/sample.mp3",
            "status": "active"
        }
        
        completed_session = meditation_guide.complete_meditation_session(session_data)
        
        return {
            "message": "瞑想セッションを完了しました",
            "session_data": completed_session
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"セッション完了エラー: {str(e)}")

@router.get("/meditation-history")
def get_meditation_history(current_user: dict = Depends(get_current_user)):
    """瞑想履歴を取得"""
    try:
        # 瞑想セッションをジャーナルから取得
        journals = SupabaseDB.get_user_journals(current_user['id'])
        meditation_sessions = [
            journal for journal in journals 
            if journal.get('session_type') == 'meditation'
        ]
        
        return {
            "sessions": meditation_sessions,
            "total_count": len(meditation_sessions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"瞑想履歴取得エラー: {str(e)}")

@router.get("/categories")
def get_meditation_categories():
    """瞑想カテゴリ一覧を取得"""
    try:
        categories = {
            "beginner": {
                "name": "初心者向け",
                "description": "瞑想を始めたばかりの方におすすめ",
                "sessions": meditation_guide.get_sessions_by_category("beginner")
            },
            "intermediate": {
                "name": "中級者向け", 
                "description": "ある程度瞑想に慣れた方におすすめ",
                "sessions": meditation_guide.get_sessions_by_category("intermediate")
            }
        }
        
        return {"categories": categories}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"カテゴリ取得エラー: {str(e)}") 