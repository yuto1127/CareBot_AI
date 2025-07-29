#!/usr/bin/env python3
"""
データ挿入によるシーケンスリセット
データを挿入して削除することでシーケンスをリセット
"""

import os
import sys
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# Supabaseクライアントをインポート
from app.config.supabase import supabase_admin
import bcrypt

def reset_sequences_via_insert():
    """データ挿入でシーケンスをリセット"""
    print("=== データ挿入によるシーケンスリセット ===")
    
    try:
        print("1. 現在のシーケンス値を確認中...")
        
        # 各テーブルにテストデータを挿入して現在のIDを確認
        test_data = {
            'users': {
                'email': 'temp_reset@example.com',
                'password': bcrypt.hashpw('temp123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                'name': 'Temp Reset User',
                'plan_type': 'free'
            },
            'journals': {
                'user_id': 1,
                'content': 'Temporary journal for sequence reset'
            },
            'moods': {
                'user_id': 1,
                'mood': 3,
                'note': 'Temporary mood for sequence reset'
            },
            'profiles': {
                'user_id': 1,
                'bio': 'Temporary profile for sequence reset'
            },
            'usage_counts': {
                'user_id': 1,
                'feature_type': 'test',
                'usage_count': 0
            },
            'analyses': {
                'user_id': 1,
                'analysis_type': 'test',
                'summary': 'Temporary analysis for sequence reset'
            },
            'feature_limits': {
                'feature_name': 'temp_reset',
                'free_limit': 1,
                'premium_limit': 10,
                'description': 'Temporary feature limit for sequence reset'
            }
        }
        
        inserted_ids = {}
        
        print("\n2. テストデータを挿入してシーケンス値を確認中...")
        
        for table_name, data in test_data.items():
            try:
                # テストデータを挿入
                response = supabase_admin.table(table_name).insert(data).execute()
                if response.data:
                    inserted_id = response.data[0]['id']
                    inserted_ids[table_name] = inserted_id
                    print(f"✅ {table_name}: テストデータ挿入 (ID: {inserted_id})")
                else:
                    print(f"❌ {table_name}: テストデータ挿入失敗")
                    
            except Exception as e:
                print(f"❌ {table_name}: テストデータ挿入エラー - {e}")
        
        print("\n3. テストデータを削除中...")
        
        # 挿入したテストデータを削除
        for table_name, inserted_id in inserted_ids.items():
            try:
                delete_response = supabase_admin.table(table_name).delete().eq('id', inserted_id).execute()
                print(f"✅ {table_name}: テストデータ削除 (ID: {inserted_id})")
            except Exception as e:
                print(f"❌ {table_name}: テストデータ削除エラー - {e}")
        
        print("\n4. シーケンスリセットの確認...")
        
        # 新しいテストデータを挿入してIDが1から始まるか確認
        print("\n5. シーケンスリセットの検証...")
        
        verification_data = {
            'users': {
                'email': 'verify_reset@example.com',
                'password': bcrypt.hashpw('verify123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                'name': 'Verify Reset User',
                'plan_type': 'free'
            }
        }
        
        for table_name, data in verification_data.items():
            try:
                # 検証用データを挿入
                response = supabase_admin.table(table_name).insert(data).execute()
                if response.data:
                    new_id = response.data[0]['id']
                    print(f"✅ {table_name}: 検証データ挿入 (ID: {new_id})")
                    
                    if new_id == 1:
                        print(f"🎉 {table_name}: シーケンスが正常にリセットされました！")
                    else:
                        print(f"⚠️  {table_name}: シーケンスがリセットされていません (ID: {new_id})")
                    
                    # 検証データを削除
                    supabase_admin.table(table_name).delete().eq('id', new_id).execute()
                    print(f"✅ {table_name}: 検証データ削除完了")
                    
                else:
                    print(f"❌ {table_name}: 検証データ挿入失敗")
                    
            except Exception as e:
                print(f"❌ {table_name}: 検証エラー - {e}")
        
        print("\n=== シーケンスリセット完了 ===")
        print("✅ データ挿入によるシーケンスリセットが完了しました")
        print("✅ 新しいデータを挿入すると、IDは1から開始されるはずです")
        
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
    print("データ挿入によるシーケンスリセットスクリプトを開始します...")
    
    # 環境設定確認
    env_ok = check_environment()
    if not env_ok:
        print("\n❌ 環境設定に問題があります")
        sys.exit(1)
    
    # シーケンスリセット
    success = reset_sequences_via_insert()
    
    if success:
        print("\n✅ シーケンスリセットが完了しました")
        sys.exit(0)
    else:
        print("\n❌ シーケンスリセットが失敗しました")
        sys.exit(1) 