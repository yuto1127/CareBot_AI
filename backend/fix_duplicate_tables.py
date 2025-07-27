#!/usr/bin/env python3
"""
重複テーブルを修正するスクリプト
"""

from app.config.supabase import supabase
import json

def migrate_data_from_old_table(old_table, new_table):
    """古いテーブルから新しいテーブルにデータを移行"""
    try:
        # 古いテーブルからデータを取得
        old_data = supabase.table(old_table).select('*').execute()
        
        if old_data.data:
            print(f"  {len(old_data.data)} 件のデータを {old_table} から {new_table} に移行中...")
            
            # 新しいテーブルにデータを挿入
            for row in old_data.data:
                try:
                    supabase.table(new_table).insert(row).execute()
                except Exception as e:
                    print(f"    データ移行エラー: {e}")
            
            print(f"  ✓ データ移行完了")
        else:
            print(f"  {old_table} にはデータがありません")
            
    except Exception as e:
        print(f"  データ移行エラー: {e}")

def create_analyses_table():
    """analysesテーブルを作成"""
    print("analysesテーブルを作成中...")
    
    # テーブル作成のSQL（Supabaseでは直接実行できないため、手動で作成する必要があります）
    create_sql = """
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
    );
    """
    
    print("以下のSQLをSupabaseダッシュボードで実行してください:")
    print(create_sql)
    print("\nまたは、SupabaseダッシュボードのTable Editorで手動でテーブルを作成してください。")

def main():
    """メイン処理"""
    print("CareBot AI 重複テーブル修正ツール")
    print("=" * 50)
    
    # 1. 使用回数テーブルの重複を修正
    print("\n=== 使用回数テーブルの修正 ===")
    print("usage_count から usage_counts に統一します")
    
    # usage_count から usage_counts にデータを移行
    migrate_data_from_old_table('usage_count', 'usage_counts')
    
    print("usage_count テーブルを削除してください（Supabaseダッシュボードから）")
    
    # 2. 機能制限テーブルの重複を修正
    print("\n=== 機能制限テーブルの修正 ===")
    print("feature_limit から feature_limits に統一します")
    
    # feature_limit から feature_limits にデータを移行
    migrate_data_from_old_table('feature_limit', 'feature_limits')
    
    print("feature_limit テーブルを削除してください（Supabaseダッシュボードから）")
    
    # 3. analysesテーブルを作成
    print("\n=== analysesテーブルの作成 ===")
    create_analyses_table()
    
    # 4. 最終確認
    print("\n=== 修正後の確認 ===")
    print("以下のテーブルが正しく設定されているか確認してください:")
    print("  ✓ users")
    print("  ✓ journals")
    print("  ✓ moods")
    print("  ✓ usage_counts (usage_count を削除)")
    print("  ✓ feature_limits (feature_limit を削除)")
    print("  ✓ analyses (新規作成)")
    print("  ✓ profiles")
    
    print("\n修正完了!")
    print("Supabaseダッシュボードで不要なテーブルを削除してください。")

if __name__ == "__main__":
    main() 