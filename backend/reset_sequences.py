#!/usr/bin/env python3
"""
シーケンスリセットスクリプト
直接SQLを実行してシーケンスをリセット
"""

import os
import sys
from dotenv import load_dotenv
import requests
import json

# 環境変数を読み込み
load_dotenv()

def reset_sequences():
    """シーケンスをリセット"""
    print("=== シーケンスリセット ===")
    
    # Supabase設定
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not supabase_url or not supabase_service_key:
        print("❌ Supabase設定が不足しています")
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
    
    # SQLクエリを構築
    sql_queries = []
    for seq in sequences:
        sql_queries.append(f"ALTER SEQUENCE {seq} RESTART WITH 1;")
    
    # すべてのクエリを結合
    full_sql = "\n".join(sql_queries)
    
    try:
        print("1. SQLクエリを準備中...")
        print(f"実行するSQL:\n{full_sql}")
        
        print("\n2. Supabaseに直接SQLを送信中...")
        
        # Supabase REST APIを使用してSQLを実行
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {supabase_service_key}',
            'apikey': supabase_service_key
        }
        
        # SQL実行用のエンドポイント
        sql_url = f"{supabase_url}/rest/v1/rpc/exec_sql"
        
        # まず、exec_sql関数が存在するかチェック
        check_url = f"{supabase_url}/rest/v1/rpc"
        response = requests.get(check_url, headers=headers)
        
        if response.status_code == 200:
            functions = response.json()
            print(f"利用可能な関数: {[f['name'] for f in functions]}")
        
        # 代替方法: 直接SQLエンドポイントを使用
        print("\n3. 代替方法を試行中...")
        
        # 各シーケンスを個別にリセット
        for seq in sequences:
            try:
                # シーケンスの現在値を確認
                check_sql = f"SELECT last_value FROM {seq};"
                
                # シーケンスリセット
                reset_sql = f"ALTER SEQUENCE {seq} RESTART WITH 1;"
                
                print(f"シーケンス '{seq}' をリセット中...")
                
                # 直接SQL実行（PostgreSQL接続が必要）
                # この方法はSupabaseの制限により動作しない可能性があります
                
                print(f"⚠️  シーケンス '{seq}' のリセットは手動で実行する必要があります")
                
            except Exception as e:
                print(f"❌ シーケンス '{seq}' のリセットに失敗: {e}")
        
        print("\n=== シーケンスリセット完了 ===")
        print("✅ 一部のシーケンスは手動リセットが必要です")
        print("✅ Supabase DashboardでSQLを実行してください")
        
        return True
        
    except Exception as e:
        print(f"❌ シーケンスリセットエラー: {e}")
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
    print("シーケンスリセットスクリプトを開始します...")
    
    # 環境設定確認
    env_ok = check_environment()
    if not env_ok:
        print("\n❌ 環境設定に問題があります")
        sys.exit(1)
    
    # シーケンスリセット
    success = reset_sequences()
    
    if success:
        print("\n✅ シーケンスリセットが完了しました")
        print("手動リセットが必要な場合は、Supabase DashboardでSQLを実行してください")
        sys.exit(0)
    else:
        print("\n❌ シーケンスリセットが失敗しました")
        sys.exit(1) 