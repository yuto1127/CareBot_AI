#!/usr/bin/env python3
"""
テストユーザー作成スクリプト
"""

import sys
import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.supabase_db import SupabaseDB
from app.schemas.auth import UserRegister

def create_test_user():
    """テストユーザーを作成"""
    print("=== テストユーザー作成 ===")
    
    try:
        # テストユーザーデータ
        test_user_data = UserRegister(
            email="test@example.com",
            username="testuser",
            password="Test1234",
            plan_type="free"
        )
        
        # データベースにユーザーを作成
        user = SupabaseDB.create_user(test_user_data)
        
        if user:
            print("✅ テストユーザー作成成功")
            print(f"ユーザーID: {user['id']}")
            print(f"メール: {user['email']}")
            print(f"ユーザー名: {user['name']}")
            print(f"プラン: {user.get('plan_type', 'free')}")
            
            # ログイン情報を表示
            print("\n=== ログイン情報 ===")
            print(f"メール: {test_user_data.email}")
            print(f"パスワード: {test_user_data.password}")
            
            return True
        else:
            print("❌ テストユーザー作成失敗")
            return False
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def check_test_user():
    """テストユーザーの存在確認"""
    print("\n=== テストユーザー確認 ===")
    
    try:
        # テストユーザーを検索
        user = SupabaseDB.get_user_by_email("test@example.com")
        
        if user:
            print("✅ テストユーザーが存在します")
            print(f"ユーザーID: {user['id']}")
            print(f"メール: {user['email']}")
            print(f"ユーザー名: {user['name']}")
            return True
        else:
            print("❌ テストユーザーが存在しません")
            return False
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def main():
    """メイン関数"""
    print("テストユーザー作成スクリプトを開始します...")
    
    # 既存のテストユーザーを確認
    if check_test_user():
        print("\nテストユーザーは既に存在します。")
        response = input("新しいテストユーザーを作成しますか？ (y/N): ")
        if response.lower() != 'y':
            print("テストユーザー作成をスキップします。")
            return
    
    # テストユーザーを作成
    if create_test_user():
        print("\n✅ テストユーザー作成が完了しました")
        print("APIテストを実行できます。")
    else:
        print("\n❌ テストユーザー作成に失敗しました")

if __name__ == "__main__":
    main() 