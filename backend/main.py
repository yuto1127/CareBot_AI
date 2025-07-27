from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router

app = FastAPI(
    title="CareBot AI API",
    description="AI-powered mental health care application",
    version="1.0.0"
)

# CORS設定（テスト段階では全URLを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # テスト段階では全URLを許可
    allow_credentials=False,  # allow_origins=["*"]の場合はFalseにする必要がある
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIルーターを追加
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to CareBot AI API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}