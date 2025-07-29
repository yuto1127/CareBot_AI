import os
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

# 必須環境変数のチェック
required_env_vars = [
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "SUPABASE_SERVICE_KEY",
    "JWT_SECRET_KEY"
]

missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"必須環境変数が設定されていません: {missing_vars}")

# 本番環境設定
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
DEBUG = ENVIRONMENT != "production"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションのライフサイクル管理"""
    # 起動時の処理
    logger.info(f"CareBot AI アプリケーションを起動中... (環境: {ENVIRONMENT})")

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
        if ENVIRONMENT == "production":
            raise
        else:
            logger.warning("開発環境のため、エラーを無視して起動を続行します")

    yield

    # 終了時の処理
    logger.info("CareBot AI アプリケーションを終了中...")

# FastAPIアプリケーションの作成
app = FastAPI(
    title="CareBot AI API",
    description="メンタルウェルネスをサポートするAIアシスタントAPI",
    version="1.0.0",
    lifespan=lifespan,
    debug=DEBUG
)

# CORS設定（開発環境と本番環境で適切なオリジンを指定）
if ENVIRONMENT == "production":
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")
    if not ALLOWED_ORIGINS or ALLOWED_ORIGINS == [""]:
        ALLOWED_ORIGINS = ["https://yourdomain.com"]  # 本番環境のドメインを指定
else:
    # 開発環境では明示的にフロントエンドのURLを指定
    ALLOWED_ORIGINS = [
        "http://localhost:5173",  # Vite開発サーバー
        "http://localhost:3000",  # 一般的な開発サーバー
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"  # フォールバック
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
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
            "version": "1.0.0",
            "environment": ENVIRONMENT
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
        "environment": ENVIRONMENT,
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn

    # ログ設定
    logger.info("開発サーバーを起動中...")

    # 本番環境では適切なホストとポートを設定
    host = "0.0.0.0" if ENVIRONMENT == "production" else "127.0.0.1"
    port = int(os.getenv("PORT", "8000"))

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=DEBUG,
        log_level="info"
    )