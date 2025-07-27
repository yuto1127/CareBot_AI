#!/usr/bin/env python3
"""
データベースの構成を維持したまま、各テーブルのデータを削除するスクリプト
"""

from app.config.supabase import supabase
import json

def clear_table_data(table_name: str):
    """指定されたテーブルのデータを削除"""
    try:
        print(f"テーブル {table_name} のデータを削除中...")
        
        # テーブルが存在するかチェック
        try:
            response = supabase.table(table_name).select('*').limit(1).execute()
            print(f"  ✓ テーブル {table_name} は存在します")
        except Exception as e:
            print(f"  ✗ テーブル {table_name} が存在しません: {e}")
            return False
        
        # データを削除
        response = supabase.table(table_name).delete().neq('id', 0).execute()
        deleted_count = len(response.data) if response.data else 0
        print(f"  ✓ {deleted_count} 件のデータを削除しました")
        return True
        
    except Exception as e:
        print(f"  ✗ データ削除エラー: {e}")
        return False

def main():
    """メイン処理"""
    print("CareBot AI データベースクリーンアップツール")
    print("=" * 50)
    print("⚠️  警告: この操作により、すべてのデータが削除されます！")
    print("   データベースの構成（テーブル構造）は維持されます。")
    print("=" * 50)
    
    # 削除対象のテーブル
    tables_to_clear = [
        'users',
        'journals', 
        'moods',
        'usage_counts',
        'feature_limits',
        'analyses',
        'profiles'
    ]
    
    # 確認
    print("\n削除対象テーブル:")
    for table in tables_to_clear:
        print(f"  - {table}")
    
    print("\nこの操作を実行しますか？ (y/N): ", end="")
    confirmation = input().strip().lower()
    
    if confirmation != 'y':
        print("操作をキャンセルしました。")
        return
    
    print("\n=== データ削除開始 ===")
    
    success_count = 0
    total_count = len(tables_to_clear)
    
    for table in tables_to_clear:
        if clear_table_data(table):
            success_count += 1
        print()
    
    print("=== 削除完了 ===")
    print(f"成功: {success_count}/{total_count} テーブル")
    
    if success_count == total_count:
        print("✅ すべてのテーブルのデータが正常に削除されました")
    else:
        print("⚠️  一部のテーブルでエラーが発生しました")
    
    print("\nデータベースが初期状態になりました。")

if __name__ == "__main__":
    main() 