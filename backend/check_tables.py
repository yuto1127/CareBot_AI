#!/usr/bin/env python3
"""
Supabaseでテーブル状況を確認するスクリプト
"""

from app.config.supabase import supabase

def check_table_exists(table_name):
    """テーブルが存在するかチェック"""
    try:
        response = supabase.table(table_name).select('*').limit(1).execute()
        return True
    except Exception as e:
        return False

def get_table_data(table_name):
    """テーブルのデータを取得"""
    try:
        response = supabase.table(table_name).select('*').limit(5).execute()
        return response.data
    except Exception as e:
        return []

def main():
    """メイン処理"""
    print("CareBot AI テーブル状況確認")
    print("=" * 40)
    
    # 確認対象のテーブル
    tables_to_check = [
        'users',
        'journals', 
        'moods',
        'usage',
        'usage_count',
        'usage_counts',
        'feature_limit',
        'feature_limits',
        'analyses',
        'profiles'
    ]
    
    existing_tables = []
    missing_tables = []
    
    for table in tables_to_check:
        if check_table_exists(table):
            existing_tables.append(table)
            data = get_table_data(table)
            print(f"✓ {table}: {len(data)} 件のデータ")
        else:
            missing_tables.append(table)
            print(f"✗ {table}: 存在しません")
    
    print(f"\n=== 結果 ===")
    print(f"存在するテーブル: {len(existing_tables)}")
    print(f"不足テーブル: {len(missing_tables)}")
    
    if existing_tables:
        print(f"\n存在するテーブル一覧:")
        for table in sorted(existing_tables):
            print(f"  - {table}")
    
    if missing_tables:
        print(f"\n不足テーブル一覧:")
        for table in sorted(missing_tables):
            print(f"  - {table}")
    
    # 重複チェック
    print(f"\n=== 重複チェック ===")
    usage_tables = [t for t in existing_tables if 'usage' in t]
    feature_tables = [t for t in existing_tables if 'feature' in t]
    
    if len(usage_tables) > 1:
        print(f"⚠️  使用回数テーブルの重複: {usage_tables}")
    
    if len(feature_tables) > 1:
        print(f"⚠️  機能制限テーブルの重複: {feature_tables}")

if __name__ == "__main__":
    main() 