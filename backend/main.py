from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.api.api import api_router
from app.database.rls_policies import rls_manager
from app.utils.logger import logger
from app.utils.error_handler import create_error_response, CareBotError

# 環境変数の読み込み
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションのライフサイクル管理"""
    # 起動時の処理
    logger.info("CareBot AI アプリケーションを起動中...")
    
    try:
        # RLSポリシーの設定
        logger.info("RLSポリシーを設定中...")
        rls_manager.setup_all_policies()
        
        # ポリシーの検証
        verification_results = rls_manager.verify_policies()
        logger.info(f"RLSポリシー検証結果: {verification_results}")
        
        logger.info("CareBot AI アプリケーションが正常に起動しました")
        
    except Exception as e:
        logger.error("アプリケーション起動エラー", e)
        raise
    
    yield
    
    # 終了時の処理
    logger.info("CareBot AI アプリケーションを終了中...")

# FastAPIアプリケーションの作成
app = FastAPI(
    title="CareBot AI API",
    description="メンタルウェルネスをサポートするAIアシスタントAPI",
    version="1.0.0",
    lifespan=lifespan
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切なオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# グローバルエラーハンドラー
@app.exception_handler(CareBotError)
async def carebot_exception_handler(request: Request, exc: CareBotError):
    """CareBotカスタムエラーハンドラー"""
    return create_error_response(exc, request)

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """一般的なエラーハンドラー"""
    return create_error_response(exc, request)

# リクエストログミドルウェア
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """リクエストログミドルウェア"""
    try:
        # リクエスト開始ログ
        logger.info(f"リクエスト開始: {request.method} {request.url.path}")
        
        # レスポンスを取得
        response = await call_next(request)
        
        # リクエスト完了ログ
        logger.info(f"リクエスト完了: {request.method} {request.url.path} - ステータス: {response.status_code}")
        
        return response
        
    except Exception as e:
        # エラーログ
        logger.error(f"リクエストエラー: {request.method} {request.url.path}", e)
        raise

# APIルーターの追加
app.include_router(api_router, prefix="/api")

# ヘルスチェックエンドポイント
@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    try:
        logger.info("ヘルスチェック実行")
        return {
            "status": "healthy",
            "message": "CareBot AI API is running",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error("ヘルスチェックエラー", e)
        raise HTTPException(status_code=500, detail="Service unhealthy")

# ルートエンドポイント
@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "CareBot AI API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    
    # ログ設定
    logger.info("開発サーバーを起動中...")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )