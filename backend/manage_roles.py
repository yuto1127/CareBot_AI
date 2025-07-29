#!/usr/bin/env python3
"""
ロール管理スクリプト
"""

import os
import sys
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# Supabaseクライアントをインポート
from app.config.supabase import supabase_admin
from app.database.supabase_db import SupabaseDB

def create_custom_roles():
    """カスタムロールを作成"""
    print("=== カスタムロール作成 ===")
    
    # カスタムロールの定義
    custom_roles = [
        {
            'name': 'admin',
            'description': 'システム管理者',
            'permissions': ['all']
        },
        {
            'name': 'premium',
            'description': 'プレミアムユーザー',
            'permissions': ['premium_features']
        },
        {
            'name': 'moderator',
            'description': 'モデレーター',
            'permissions': ['moderate_content']
        }
    ]
    
    try:
        for role in custom_roles:
            print(f"ロール '{role['name']}' を作成中...")
            
            # ロールが存在するかチェック
            check_query = f"SELECT rolname FROM pg_roles WHERE rolname = '{role['name']}'"
            result = supabase_admin.rpc('exec_sql', {'sql': check_query}).execute()
            
            if not result.data:
                # ロールを作成
                create_query = f"CREATE ROLE {role['name']}"
                supabase_admin.rpc('exec_sql', {'sql': create_query}).execute()
                print(f"✅ ロール '{role['name']}' を作成しました")
            else:
                print(f"⚠️  ロール '{role['name']}' は既に存在します")
        
        print("=== カスタムロール作成完了 ===")
        return True
        
    except Exception as e:
        print(f"❌ ロール作成エラー: {e}")
        return False

def assign_role_to_user(email: str, role: str):
    """ユーザーにロールを割り当て"""
    print(f"=== ユーザー '{email}' にロール '{role}' を割り当て ===")
    
    try:
        # ユーザーを検索
        user = SupabaseDB.get_user_by_email(email)
        if not user:
            print(f"❌ ユーザー '{email}' が見つかりません")
            return False
        
        # ロールを更新
        updated_user = SupabaseDB.update_user_role(
            user_id=user['id'],
            role=role,
            updated_by=1,  # システム管理者
            reason="スクリプトによるロール割り当て"
        )
        
        if updated_user:
            print(f"✅ ユーザー '{email}' にロール '{role}' を割り当てました")
            return True
        else:
            print(f"❌ ロール割り当てに失敗しました")
            return False
            
    except Exception as e:
        print(f"❌ ロール割り当てエラー: {e}")
        return False

def list_users_by_role(role: str = None):
    """ロール別ユーザー一覧を表示"""
    print("=== ユーザー一覧 ===")
    
    try:
        if role:
            users = SupabaseDB.get_user_by_role(role)
            print(f"ロール '{role}' のユーザー:")
        else:
            users = SupabaseDB.get_all_users()
            print("すべてのユーザー:")
        
        for user in users:
            print(f"  - ID: {user['id']}, Email: {user['email']}, Name: {user['name']}, Role: {user.get('role', 'authenticated')}, Plan: {user.get('plan_type', 'free')}")
        
        print(f"合計: {len(users)}人")
        
    except Exception as e:
        print(f"❌ ユーザー一覧取得エラー: {e}")

def get_role_statistics():
    """ロール別統計を表示"""
    print("=== ロール別統計 ===")
    
    try:
        roles = ['authenticated', 'admin', 'premium', 'moderator']
        
        for role in roles:
            stats = SupabaseDB.get_user_stats_by_role(role)
            print(f"ロール '{role}':")
            print(f"  - 総ユーザー数: {stats['total_users']}")
            print(f"  - アクティブユーザー: {stats['active_users']}")
            print(f"  - プレミアムユーザー: {stats['premium_users']}")
            print(f"  - 無料ユーザー: {stats['free_users']}")
            print()
        
    except Exception as e:
        print(f"❌ 統計取得エラー: {e}")

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

def show_usage():
    """使用方法を表示"""
    print("=== ロール管理スクリプト使用方法 ===")
    print()
    print("1. カスタムロール作成:")
    print("   python manage_roles.py create-roles")
    print()
    print("2. ユーザーにロール割り当て:")
    print("   python manage_roles.py assign <email> <role>")
    print("   例: python manage_roles.py assign admin@example.com admin")
    print()
    print("3. ユーザー一覧表示:")
    print("   python manage_roles.py list [role]")
    print("   例: python manage_roles.py list admin")
    print()
    print("4. 統計表示:")
    print("   python manage_roles.py stats")
    print()
    print("利用可能なロール:")
    print("  - authenticated: 認証済みユーザー")
    print("  - admin: 管理者")
    print("  - premium: プレミアムユーザー")
    print("  - moderator: モデレーター")

if __name__ == "__main__":
    print("ロール管理スクリプトを開始します...")
    
    # 環境設定確認
    env_ok = check_environment()
    if not env_ok:
        print("\n❌ 環境設定に問題があります")
        sys.exit(1)
    
    # コマンドライン引数の処理
    if len(sys.argv) < 2:
        show_usage()
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "create-roles":
        success = create_custom_roles()
        sys.exit(0 if success else 1)
        
    elif command == "assign":
        if len(sys.argv) < 4:
            print("❌ 使用方法: python manage_roles.py assign <email> <role>")
            sys.exit(1)
        
        email = sys.argv[2]
        role = sys.argv[3]
        success = assign_role_to_user(email, role)
        sys.exit(0 if success else 1)
        
    elif command == "list":
        role = sys.argv[2] if len(sys.argv) > 2 else None
        list_users_by_role(role)
        sys.exit(0)
        
    elif command == "stats":
        get_role_statistics()
        sys.exit(0)
        
    else:
        print(f"❌ 不明なコマンド: {command}")
        show_usage()
        sys.exit(1) 