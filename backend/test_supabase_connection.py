#!/usr/bin/env python3
"""
Supabase接続テストスクリプト（本番環境向け）
"""

import os
import sys
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# Supabaseクライアントをインポート
from app.config.supabase import supabase, supabase_admin

def test_supabase_connection():
    """Supabase接続をテスト"""
    print("=== Supabase接続テスト（本番環境向け） ===")
    
    try:
        # 基本的な接続テスト
        print("1. 基本的な接続テスト...")
        response = supabase_admin.table('users').select('count').limit(1).execute()
        print(f"✅ 接続成功: {response}")
        
        # usersテーブルの構造確認
        print("\n2. usersテーブル構造確認...")
        response = supabase_admin.table('users').select('*').limit(1).execute()
        print(f"✅ テーブル構造: {response}")
        
        # 既存データの確認
        print("\n3. 既存データ確認...")
        response = supabase_admin.table('users').select('*').execute()
        print(f"✅ 既存データ数: {len(response.data) if response.data else 0}")
        if response.data:
            print(f"✅ データ例: {response.data[0] if response.data else 'なし'}")
        
        # テスト挿入
        print("\n4. テスト挿入...")
        test_data = {
            'email': 'test_connection@example.com',
            'password': 'hashed_test_password',
            'name': 'Test Connection User',
            'plan_type': 'free'
        }
        
        insert_response = supabase_admin.table('users').insert(test_data).execute()
        print(f"✅ 挿入テスト結果: {insert_response}")
        
        if insert_response.data:
            print(f"✅ 挿入成功: {insert_response.data[0]}")
            
            # 挿入したデータを削除
            user_id = insert_response.data[0]['id']
            delete_response = supabase_admin.table('users').delete().eq('id', user_id).execute()
            print(f"✅ テストデータ削除: {delete_response}")
        else:
            print("❌ 挿入失敗")
        
        print("\n=== テスト完了 ===")
        return True
        
    except Exception as e:
        print(f"❌ 接続エラー: {e}")
        print(f"エラータイプ: {type(e)}")
        return False

def check_environment():
    """環境設定を確認"""
    print("=== 環境設定確認 ===")
    
    env = os.getenv("ENVIRONMENT", "development")
    supabase_url = os.getenv("SUPABASE_URL", "not set")
    supabase_key = os.getenv("SUPABASE_KEY", "not set")
    supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY", "not set")
    
    print(f"環境: {env}")
    print(f"Supabase URL: {supabase_url}")
    print(f"Supabase Key: {supabase_key[:20]}..." if len(supabase_key) > 20 else supabase_key)
    print(f"Supabase Service Key: {supabase_service_key[:20]}..." if len(supabase_service_key) > 20 else supabase_service_key)
    
    # 必須環境変数のチェック
    missing_vars = []
    if not os.getenv("SUPABASE_URL"):
        missing_vars.append("SUPABASE_URL")
    if not os.getenv("SUPABASE_KEY"):
        missing_vars.append("SUPABASE_KEY")
    if not os.getenv("SUPABASE_SERVICE_KEY"):
        missing_vars.append("SUPABASE_SERVICE_KEY")
    
    if missing_vars:
        print(f"❌ 不足している環境変数: {missing_vars}")
        return False
    else:
        print("✅ すべての必須環境変数が設定されています")
        return True

if __name__ == "__main__":
    print("Supabase接続テストを開始します...")
    
    # 環境設定確認
    env_ok = check_environment()
    if not env_ok:
        print("\n❌ 環境設定に問題があります")
        sys.exit(1)
    
    # 接続テスト
    success = test_supabase_connection()
    
    if success:
        print("\n✅ すべてのテストが成功しました")
        sys.exit(0)
    else:
        print("\n❌ テストが失敗しました")
        sys.exit(1) 