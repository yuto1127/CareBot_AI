#!/usr/bin/env python3
"""
PostgreSQL直接接続でシーケンスリセット
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2
from urllib.parse import urlparse

# 環境変数を読み込み
load_dotenv()

def get_connection_string():
    """Supabase URLからPostgreSQL接続文字列を生成"""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not supabase_url or not supabase_service_key:
        return None
    
    # Supabase URLからホストとポートを抽出
    parsed = urlparse(supabase_url)
    host = parsed.hostname
    port = parsed.port or 5432
    
    # データベース名を抽出（通常はpostgres）
    db_name = "postgres"
    
    # 接続文字列を構築
    conn_string = f"host={host} port={port} dbname={db_name} user=postgres password={supabase_service_key} sslmode=require"
    
    return conn_string

def reset_sequences_psql():
    """PostgreSQL直接接続でシーケンスをリセット"""
    print("=== PostgreSQL直接接続でシーケンスリセット ===")
    
    # 接続文字列を取得
    conn_string = get_connection_string()
    if not conn_string:
        print("❌ 接続文字列の生成に失敗しました")
        return False
    
    # リセット対象のシーケンス
    sequences = [
        'analyses_id_seq',
        'feature_limits_id_seq',
        'journals_id_seq', 
        'moods_id_seq',
        'profiles_id_seq',
        'usage_counts_id_seq',
        'users_id_seq'
    ]
    
    try:
        print("1. PostgreSQLに接続中...")
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        print("✅ PostgreSQLに接続しました")
        
        print("\n2. シーケンスをリセット中...")
        
        for seq in sequences:
            try:
                # シーケンスの現在値を確認
                cursor.execute(f"SELECT last_value FROM {seq}")
                current_value = cursor.fetchone()[0]
                print(f"シーケンス '{seq}' の現在値: {current_value}")
                
                # シーケンスをリセット
                cursor.execute(f"ALTER SEQUENCE {seq} RESTART WITH 1")
                print(f"✅ シーケンス '{seq}' をリセットしました")
                
            except Exception as e:
                print(f"❌ シーケンス '{seq}' のリセットに失敗: {e}")
        
        # 変更をコミット
        conn.commit()
        print("\n✅ すべての変更をコミットしました")
        
        # 接続を閉じる
        cursor.close()
        conn.close()
        print("✅ データベース接続を閉じました")
        
        print("\n=== シーケンスリセット完了 ===")
        print("✅ すべてのシーケンスが1から再開されるように設定されました")
        
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL接続エラー: {e}")
        return False

def check_environment():
    """環境設定を確認"""
    print("=== 環境設定確認 ===")
    
    env = os.getenv("ENVIRONMENT", "development")
    supabase_url = os.getenv("SUPABASE_URL", "not set")
    supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY", "not set")
    
    print(f"環境: {env}")
    print(f"Supabase URL: {supabase_url}")
    print(f"Supabase Service Key: {supabase_service_key[:20]}..." if len(supabase_service_key) > 20 else supabase_service_key)
    
    # 必須環境変数のチェック
    missing_vars = []
    if not os.getenv("SUPABASE_URL"):
        missing_vars.append("SUPABASE_URL")
    if not os.getenv("SUPABASE_SERVICE_KEY"):
        missing_vars.append("SUPABASE_SERVICE_KEY")
    
    if missing_vars:
        print(f"❌ 不足している環境変数: {missing_vars}")
        return False
    else:
        print("✅ すべての必須環境変数が設定されています")
        return True

if __name__ == "__main__":
    print("PostgreSQL直接接続シーケンスリセットスクリプトを開始します...")
    
    # 環境設定確認
    env_ok = check_environment()
    if not env_ok:
        print("\n❌ 環境設定に問題があります")
        sys.exit(1)
    
    # シーケンスリセット
    success = reset_sequences_psql()
    
    if success:
        print("\n✅ シーケンスリセットが完了しました")
        sys.exit(0)
    else:
        print("\n❌ シーケンスリセットが失敗しました")
        sys.exit(1) 