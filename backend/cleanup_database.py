#!/usr/bin/env python3
"""
データベースの重複テーブルを整理するスクリプト
"""

from app.config.supabase import supabase
import json

def list_all_tables():
    """すべてのテーブルを一覧表示"""
    try:
        # システムテーブルを除いたテーブル一覧を取得
        response = supabase.table('information_schema.tables').select('table_name').eq('table_schema', 'public').execute()
        tables = [row['table_name'] for row in response.data]
        print("現在のテーブル一覧:")
        for table in sorted(tables):
            print(f"  - {table}")
        return tables
    except Exception as e:
        print(f"テーブル一覧取得エラー: {e}")
        return []

def check_table_structure(table_name):
    """テーブルの構造を確認"""
    try:
        # テーブルの列情報を取得
        response = supabase.table('information_schema.columns').select('column_name,data_type,is_nullable').eq('table_schema', 'public').eq('table_name', table_name).execute()
        columns = response.data
        print(f"\n{table_name} テーブルの構造:")
        for col in columns:
            print(f"  - {col['column_name']}: {col['data_type']} ({'NULL' if col['is_nullable'] == 'YES' else 'NOT NULL'})")
        return columns
    except Exception as e:
        print(f"テーブル構造確認エラー: {e}")
        return []

def cleanup_duplicate_tables():
    """重複テーブルを整理"""
    print("=== データベースクリーンアップ開始 ===")
    
    # 現在のテーブル一覧を取得
    tables = list_all_tables()
    
    # 重複テーブルの定義
    duplicate_groups = {
        'usage': ['usage', 'usage_count', 'usage_counts'],
        'feature_limits': ['feature_limit', 'feature_limits']
    }
    
    # 各重複グループを処理
    for group_name, table_list in duplicate_groups.items():
        print(f"\n=== {group_name} グループの処理 ===")
        
        # 存在するテーブルを確認
        existing_tables = [t for t in table_list if t in tables]
        
        if len(existing_tables) > 1:
            print(f"重複テーブルを発見: {existing_tables}")
            
            # 正しいテーブル名を決定
            if group_name == 'usage':
                correct_table = 'usage_counts'  # 新しい命名規則に合わせる
            elif group_name == 'feature_limits':
                correct_table = 'feature_limits'  # 複数形に統一
            else:
                correct_table = existing_tables[0]
            
            print(f"正しいテーブル名: {correct_table}")
            
            # 不要なテーブルを削除
            for table in existing_tables:
                if table != correct_table:
                    print(f"削除対象: {table}")
                    try:
                        # テーブル削除（注意: データが失われます）
                        response = supabase.rpc('drop_table_if_exists', {'table_name': table}).execute()
                        print(f"  ✓ {table} を削除しました")
                    except Exception as e:
                        print(f"  ✗ {table} の削除に失敗: {e}")
        else:
            print(f"重複なし: {existing_tables}")

def create_missing_tables():
    """不足しているテーブルを作成"""
    print("\n=== 不足テーブルの作成 ===")
    
    # 必要なテーブル定義
    required_tables = {
        'users': '''
            CREATE TABLE IF NOT EXISTS users (
                id BIGSERIAL PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT,
                plan_type TEXT DEFAULT 'free',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        ''',
        'journals': '''
            CREATE TABLE IF NOT EXISTS journals (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT REFERENCES users(id),
                content TEXT NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        ''',
        'moods': '''
            CREATE TABLE IF NOT EXISTS moods (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT REFERENCES users(id),
                mood INTEGER NOT NULL CHECK (mood >= 1 AND mood <= 5),
                note TEXT,
                recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        ''',
        'usage_counts': '''
            CREATE TABLE IF NOT EXISTS usage_counts (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT REFERENCES users(id),
                feature TEXT NOT NULL,
                usage_count INTEGER DEFAULT 0,
                last_used TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        ''',
        'analyses': '''
            CREATE TABLE IF NOT EXISTS analyses (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT REFERENCES users(id),
                analysis_type TEXT NOT NULL,
                summary TEXT NOT NULL,
                insights TEXT NOT NULL,
                recommendations TEXT NOT NULL,
                mood_score FLOAT,
                stress_level TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        '''
    }
    
    for table_name, create_sql in required_tables.items():
        try:
            print(f"テーブル {table_name} を確認中...")
            # テーブルが存在するかチェック
            response = supabase.table(table_name).select('*').limit(1).execute()
            print(f"  ✓ {table_name} は既に存在します")
        except Exception as e:
            print(f"  ✗ {table_name} が存在しません: {e}")
            print(f"  作成SQL: {create_sql.strip()}")

def main():
    """メイン処理"""
    print("CareBot AI データベースクリーンアップツール")
    print("=" * 50)
    
    # 1. 現在のテーブル状況を確認
    tables = list_all_tables()
    
    # 2. 重複テーブルを整理
    cleanup_duplicate_tables()
    
    # 3. 不足テーブルを確認
    create_missing_tables()
    
    # 4. 最終確認
    print("\n=== 最終確認 ===")
    final_tables = list_all_tables()
    
    print("\nクリーンアップ完了!")
    print(f"最終テーブル数: {len(final_tables)}")

if __name__ == "__main__":
    main() 