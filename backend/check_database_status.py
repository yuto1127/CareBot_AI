#!/usr/bin/env python3
"""
データベース状態確認スクリプト
"""

import os
import sys
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# Supabaseクライアントをインポート
from app.config.supabase import supabase_admin

def check_database_status():
    """データベースの状態を確認"""
    print("=== データベース状態確認 ===")
    
    # 確認対象のテーブル
    tables = [
        'analyses',
        'feature_limits', 
        'journals',
        'moods',
        'profiles',
        'usage_counts',
        'users'
    ]
    
    try:
        print("\n1. 各テーブルのデータ数を確認:")
        for table in tables:
            try:
                response = supabase_admin.table(table).select('*').execute()
                count = len(response.data) if response.data else 0
                print(f"  - {table}: {count} 件")
            except Exception as e:
                print(f"  - {table}: エラー - {e}")
        
        print("\n2. 最新のデータを確認:")
        for table in tables:
            try:
                response = supabase_admin.table(table).select('*').order('id', desc=True).limit(1).execute()
                if response.data:
                    latest = response.data[0]
                    print(f"  - {table}: ID {latest.get('id', 'N/A')}")
                else:
                    print(f"  - {table}: データなし")
            except Exception as e:
                print(f"  - {table}: エラー - {e}")
        
        print("\n3. テストデータ挿入:")
        # テストユーザーを作成
        try:
            test_user = {
                'email': 'test@example.com',
                'password': 'hashed_password',
                'name': 'Test User',
                'plan_type': 'free'
            }
            
            response = supabase_admin.table('users').insert(test_user).execute()
            if response.data:
                new_id = response.data[0]['id']
                print(f"✅ テストユーザーを作成しました (ID: {new_id})")
                
                # テストデータを削除
                supabase_admin.table('users').delete().eq('id', new_id).execute()
                print(f"✅ テストユーザーを削除しました (ID: {new_id})")
            else:
                print("❌ テストユーザーの作成に失敗しました")
                
        except Exception as e:
            print(f"❌ テストデータ挿入エラー: {e}")
        
        print("\n=== データベース状態確認完了 ===")
        return True
        
    except Exception as e:
        print(f"❌ データベース状態確認エラー: {e}")
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
    print("データベース状態確認スクリプトを開始します...")
    
    # 環境設定確認
    env_ok = check_environment()
    if not env_ok:
        print("\n❌ 環境設定に問題があります")
        sys.exit(1)
    
    # データベース状態確認
    success = check_database_status()
    
    if success:
        print("\n✅ データベース状態確認が完了しました")
        sys.exit(0)
    else:
        print("\n❌ データベース状態確認が失敗しました")
        sys.exit(1) 