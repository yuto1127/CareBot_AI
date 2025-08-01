"""
CBT対話APIエンドポイント
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Dict, Any
from app.schemas.cbt import (
    CBTRequest, CBTResponse, CBTSessionRequest, CBTSessionResponse,
    CBTConversationHistory, CBTQualityReport
)
from app.utils.auth import get_current_user
from app.utils.ai_engine import LightweightAIEngine, AIQualityMonitor
from app.utils.logger import logger
from app.utils.error_handler import (
    ValidationError, DatabaseError,
    create_error_response, log_request_info, validate_required_fields
)
from app.database.supabase_db import SupabaseDB
import uuid
from datetime import datetime

router = APIRouter(tags=["cbt"])

# AIエンジンのインスタンス（グローバルで管理）
ai_engine = LightweightAIEngine()
quality_monitor = AIQualityMonitor()

@router.post("/session", response_model=CBTSessionResponse)
async def start_cbt_session(
    request: CBTSessionRequest,
    current_user: dict = Depends(get_current_user),
    request_obj: Request = None
):
    """CBTセッションを開始"""
    try:
        if request_obj:
            log_request_info(request_obj, current_user['id'])
        
        # セッションIDを生成
        session_id = str(uuid.uuid4())
        
        # 歓迎メッセージ
        welcome_message = """
こんにちは！私はあなたのメンタルウェルネスをサポートするAIコーチです。
認知行動療法（CBT）の原則に基づいて、あなたの思考プロセスを整理するお手伝いをします。

何でもお気軽にお話しください。あなたの気持ちや考えを聞かせてください。
"""
        
        # 初期メッセージがある場合は処理
        if request.initial_message:
            ai_response = ai_engine.process_message(request.initial_message, current_user['id'])
            welcome_message += f"\n\nあなた: {request.initial_message}\n\n私: {ai_response['response']}"
        
        logger.log_user_action(
            user_id=current_user['id'],
            action="start_cbt_session"
        )
        
        return CBTSessionResponse(
            session_id=session_id,
            welcome_message=welcome_message,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error("CBTセッション開始エラー", e, {"user_id": current_user['id']})
        if request_obj:
            raise create_error_response(e, request_obj)
        else:
            raise HTTPException(status_code=500, detail="セッションの開始に失敗しました")

@router.post("/conversation", response_model=CBTResponse)
async def cbt_conversation(
    request: CBTRequest,
    current_user: dict = Depends(get_current_user),
    request_obj: Request = None
):
    """CBT対話セッション"""
    try:
        if request_obj:
            log_request_info(request_obj, current_user['id'])
        
        # 入力検証
        validate_required_fields(request.dict(), ["message"])
        
        # AIエンジンでメッセージを処理
        ai_response = ai_engine.process_message(request.message, current_user['id'])
        
        # 品質監視に記録
        quality_monitor.log_conversation(
            user_input=request.message,
            ai_response=ai_response['response'],
            emotion=ai_response['emotion'],
            crisis_detected=ai_response['crisis_detected']
        )
        
        # ジャーナルとして記録（危機的状況でない場合）
        if not ai_response['crisis_detected']:
            try:
                await record_cbt_conversation(
                    user_id=current_user['id'],
                    message=request.message,
                    response=ai_response['response'],
                    emotion=ai_response['emotion'],
                    session_id=request.session_id
                )
            except Exception as e:
                logger.error("CBT対話記録エラー", e, {"user_id": current_user['id']})
                # 記録エラーは対話自体には影響しない
        
        logger.log_user_action(
            user_id=current_user['id'],
            action="cbt_conversation"
        )
        
        return CBTResponse(
            message=ai_response['response'],
            emotion=ai_response['emotion'],
            crisis_detected=ai_response['crisis_detected'],
            session_id=request.session_id,
            timestamp=ai_response['timestamp'],
            context=ai_response['context']
        )
        
    except ValidationError as e:
        if request_obj:
            raise create_error_response(e, request_obj)
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("CBT対話エラー", e, {"user_id": current_user['id']})
        if request_obj:
            raise create_error_response(e, request_obj)
        else:
            raise HTTPException(status_code=500, detail="対話の処理中にエラーが発生しました")

@router.get("/conversation/summary", response_model=str)
async def get_conversation_summary(
    current_user: dict = Depends(get_current_user),
    request_obj: Request = None
):
    """対話の要約を取得"""
    try:
        if request_obj:
            log_request_info(request_obj, current_user['id'])
        
        summary = ai_engine.get_conversation_summary()
        
        logger.log_user_action(
            user_id=current_user['id'],
            action="get_conversation_summary"
        )
        
        return summary
        
    except Exception as e:
        logger.error("対話要約取得エラー", e, {"user_id": current_user['id']})
        if request_obj:
            raise create_error_response(e, request_obj)
        else:
            raise HTTPException(status_code=500, detail="対話要約の取得に失敗しました")

@router.get("/quality/report", response_model=CBTQualityReport)
async def get_quality_report(
    current_user: dict = Depends(get_current_user),
    request_obj: Request = None
):
    """AI品質レポートを取得"""
    try:
        if request_obj:
            log_request_info(request_obj, current_user['id'])
        
        # 管理者のみアクセス可能
        if current_user.get('role') != 'admin':
            raise HTTPException(status_code=403, detail="管理者権限が必要です")
        
        report = quality_monitor.get_quality_report()
        report['timestamp'] = datetime.now().isoformat()
        
        logger.log_user_action(
            user_id=current_user['id'],
            action="get_quality_report"
        )
        
        return CBTQualityReport(**report)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("品質レポート取得エラー", e, {"user_id": current_user['id']})
        if request_obj:
            raise create_error_response(e, request_obj)
        else:
            raise HTTPException(status_code=500, detail="品質レポートの取得に失敗しました")

async def record_cbt_conversation(
    user_id: int,
    message: str,
    response: str,
    emotion: str,
    session_id: str = None
):
    """CBT対話をジャーナルとして記録"""
    try:
        # ジャーナルテーブルに記録
        journal_data = {
            "user_id": user_id,
            "content": f"【CBT対話】\nユーザー: {message}\nAI: {response}\n感情: {emotion}",
            "cbt_session_id": session_id,
            "emotion": emotion
        }
        
        SupabaseDB.create_journal(journal_data)
        
    except Exception as e:
        logger.error("CBT対話記録エラー", e, {"user_id": user_id})
        raise DatabaseError("CBT対話の記録に失敗しました") 