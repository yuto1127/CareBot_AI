import os
from supabase import create_client, Client
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# Supabase設定（環境変数から取得）
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# 必須環境変数のチェック
if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL環境変数が設定されていません")
if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY環境変数が設定されていません")
if not SUPABASE_SERVICE_KEY:
    raise ValueError("SUPABASE_SERVICE_KEY環境変数が設定されていません")

# Supabaseクライアントの初期化（anon key）
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# service_roleキーを使用してRLSをバイパスするクライアント
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY) 