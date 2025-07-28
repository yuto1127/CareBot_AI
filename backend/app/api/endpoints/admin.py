from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from ...database.rls_policies import rls_manager
from ...database.supabase_db import SupabaseDB
from ...utils.logger import logger
from ...utils.error_handler import handle_carebot_error

router = APIRouter(tags=["admin"])

@router.get("/rls-status")
async def get_rls_status():
    """RLS設定状況を取得"""
    try:
        logger.info("RLS設定状況の確認を開始")
        
        # ポリシー状況を取得
        status = rls_manager.get_policy_status()
        
        # 検証結果も取得
        verification = rls_manager.verify_policies()
        
        result = {
            "policy_status": status,
            "verification": verification,
            "summary": {
                "total_tables": len(status),
                "configured_tables": sum(1 for s in status.values() if s.get("status") == "configured"),
                "error_tables": sum(1 for s in status.values() if s.get("status") == "error")
            }
        }
        
        logger.info("RLS設定状況の確認完了", result)
        return result
        
    except Exception as e:
        handle_carebot_error(e, "RLS設定状況の取得に失敗しました")

@router.post("/rls-setup")
async def setup_rls():
    """RLS設定を実行"""
    try:
        logger.info("RLS設定の実行を開始")
        
        # RLS設定を実行
        rls_manager.setup_all_policies()
        
        # 設定後の検証
        verification = rls_manager.verify_policies()
        
        result = {
            "message": "RLS設定が完了しました",
            "verification": verification,
            "setup_completed": True
        }
        
        logger.info("RLS設定の実行完了", result)
        return result
        
    except Exception as e:
        handle_carebot_error(e, "RLS設定の実行に失敗しました")

@router.get("/table-structure")
async def get_table_structure():
    """テーブル構造を確認"""
    try:
        logger.info("テーブル構造の確認を開始")
        
        # テーブル構造を確認
        db = SupabaseDB()
        structure = db.check_user_id_types()
        
        result = {
            "table_structures": structure,
            "message": "テーブル構造の確認完了"
        }
        
        logger.info("テーブル構造の確認完了", result)
        return result
        
    except Exception as e:
        handle_carebot_error(e, "テーブル構造の確認に失敗しました") 