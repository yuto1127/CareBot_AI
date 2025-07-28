from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from app.utils.auth import get_current_user
from app.database.supabase_db import SupabaseDB
from app.utils.logger import logger
from app.utils.error_handler import create_error_response, log_request_info

router = APIRouter(tags=["users"])

# 基本的なユーザー管理機能
# 詳細なプロフィール機能は profiles.py で管理 