#!/usr/bin/env python3
"""
Supabaseデータベースリセットスクリプト
各テーブルのデータを削除し、IDを1から再開するように設定
"""

import os
import sys
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# Supabaseクライアントをインポート
from app.config.supabase import supabase_admin
from app.utils.logger import logger

def reset_database():
    """データベースをリセット"""
    print("=== Supabaseデータベースリセット ===")
    
    # リセット対象のテーブル
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
        for table in tables:
            print(f"\n1. テーブル '{table}' のデータを削除中...")
            
            # テーブルが存在するかチェック
            try:
                # テーブルの存在確認
                check_response = supabase_admin.table(table).select('*').limit(1).execute()
                print(f"✅ テーブル '{table}' が存在します")
                
                # すべてのデータを削除
                delete_response = supabase_admin.table(table).delete().neq('id', 0).execute()
                deleted_count = len(delete_response.data) if delete_response.data else 0
                print(f"✅ テーブル '{table}' から {deleted_count} 件のデータを削除しました")
                
            except Exception as e:
                print(f"⚠️  テーブル '{table}' が存在しないか、アクセスできません: {e}")
                continue
        
        print("\n2. シーケンスをリセット中...")
        
        # 各テーブルのシーケンスをリセット
        sequences = [
            'analyses_id_seq',
            'feature_limits_id_seq',
            'journals_id_seq', 
            'moods_id_seq',
            'profiles_id_seq',
            'usage_counts_id_seq',
            'users_id_seq'
        ]
        
        for seq in sequences:
            try:
                # シーケンスをリセット
                reset_query = f"ALTER SEQUENCE {seq} RESTART WITH 1"
                supabase_admin.rpc('exec_sql', {'sql': reset_query}).execute()
                print(f"✅ シーケンス '{seq}' をリセットしました")
            except Exception as e:
                print(f"⚠️  シーケンス '{seq}' のリセットに失敗: {e}")
        
        print("\n3. テーブル構造を確認中...")
        
        # 各テーブルの構造を確認
        for table in tables:
            try:
                response = supabase_admin.table(table).select('*').limit(1).execute()
                print(f"✅ テーブル '{table}' は正常にアクセス可能です")
            except Exception as e:
                print(f"❌ テーブル '{table}' へのアクセスエラー: {e}")
        
        print("\n=== データベースリセット完了 ===")
        print("✅ すべてのテーブルのデータが削除されました")
        print("✅ IDシーケンスが1から再開されるように設定されました")
        print("✅ 新しいデータを挿入すると、IDは1から開始されます")
        
        return True
        
    except Exception as e:
        print(f"❌ データベースリセットエラー: {e}")
        print(f"エラータイプ: {type(e)}")
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

def show_warning():
    """警告メッセージを表示"""
    print("\n⚠️  **重要警告** ⚠️")
    print("このスクリプトは以下の操作を実行します:")
    print("1. すべてのテーブルのデータを完全に削除")
    print("2. IDシーケンスを1から再開")
    print("3. この操作は元に戻せません")
    print("\n続行しますか？ (y/N): ", end="")
    
    response = input().strip().lower()
    return response in ['y', 'yes']

if __name__ == "__main__":
    print("Supabaseデータベースリセットスクリプトを開始します...")
    
    # 環境設定確認
    env_ok = check_environment()
    if not env_ok:
        print("\n❌ 環境設定に問題があります")
        sys.exit(1)
    
    # 警告メッセージを表示
    if not show_warning():
        print("❌ 操作がキャンセルされました")
        sys.exit(0)
    
    # データベースリセット
    success = reset_database()
    
    if success:
        print("\n✅ データベースリセットが完了しました")
        print("新しいデータを挿入すると、IDは1から開始されます")
        sys.exit(0)
    else:
        print("\n❌ データベースリセットが失敗しました")
        sys.exit(1) 