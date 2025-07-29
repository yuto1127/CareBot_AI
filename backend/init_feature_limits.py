#!/usr/bin/env python3
"""
機能制限の初期データ設定スクリプト
"""

import os
import sys
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# Supabaseクライアントをインポート
from app.config.supabase import supabase_admin

def init_feature_limits():
    """機能制限の初期データを設定"""
    print("=== 機能制限の初期データ設定 ===")
    
    # 機能制限の初期データ
    feature_limits = [
        {
            'feature_name': 'journal',
            'free_limit': 10,
            'premium_limit': 100,
            'description': 'ジャーナル作成回数'
        },
        {
            'feature_name': 'mood',
            'free_limit': 30,
            'premium_limit': 300,
            'description': '気分記録作成回数'
        },
        {
            'feature_name': 'cbt',
            'free_limit': 5,
            'premium_limit': 50,
            'description': 'CBTセッション回数'
        },
        {
            'feature_name': 'meditation',
            'free_limit': 10,
            'premium_limit': 100,
            'description': '瞑想セッション回数'
        },
        {
            'feature_name': 'sounds',
            'free_limit': 20,
            'premium_limit': 200,
            'description': 'リラクゼーションサウンド使用回数'
        },
        {
            'feature_name': 'pomodoro',
            'free_limit': 50,
            'premium_limit': 500,
            'description': 'ポモドーロタイマー使用回数'
        },
        {
            'feature_name': 'analysis',
            'free_limit': 3,
            'premium_limit': 30,
            'description': 'AI分析回数'
        }
    ]
    
    try:
        # 既存のデータを削除
        print("1. 既存の機能制限データを削除中...")
        delete_response = supabase_admin.table('feature_limits').delete().neq('id', 0).execute()
        print(f"✅ 削除完了: {len(delete_response.data) if delete_response.data else 0}件")
        
        # 新しいデータを挿入
        print("\n2. 新しい機能制限データを挿入中...")
        for feature in feature_limits:
            insert_response = supabase_admin.table('feature_limits').insert(feature).execute()
            if insert_response.data:
                print(f"✅ {feature['feature_name']}: 無料{feature['free_limit']}回, プレミアム{feature['premium_limit']}回")
            else:
                print(f"❌ {feature['feature_name']}: 挿入失敗")
        
        # 確認
        print("\n3. 設定された機能制限を確認中...")
        check_response = supabase_admin.table('feature_limits').select('*').execute()
        print(f"✅ 設定完了: {len(check_response.data)}件の機能制限")
        
        for feature in check_response.data:
            print(f"  - {feature['feature_name']}: 無料{feature['free_limit']}回, プレミアム{feature['premium_limit']}回")
        
        print("\n=== 機能制限の初期データ設定完了 ===")
        return True
        
    except Exception as e:
        print(f"❌ 機能制限設定エラー: {e}")
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

if __name__ == "__main__":
    print("機能制限の初期データ設定を開始します...")
    
    # 環境設定確認
    env_ok = check_environment()
    if not env_ok:
        print("\n❌ 環境設定に問題があります")
        sys.exit(1)
    
    # 機能制限設定
    success = init_feature_limits()
    
    if success:
        print("\n✅ 機能制限の初期データ設定が完了しました")
        sys.exit(0)
    else:
        print("\n❌ 機能制限の初期データ設定が失敗しました")
        sys.exit(1) 