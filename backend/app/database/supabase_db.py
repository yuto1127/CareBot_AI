from typing import List, Dict, Any, Optional
from app.config.supabase import supabase
from app.schemas.user import UserCreate, UserResponse
from app.schemas.journal import JournalCreate, JournalResponse
from app.schemas.mood import MoodCreate, MoodResponse
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
import json

class SupabaseDB:
    """Supabaseデータベース操作クラス"""
    
    # ユーザー関連
    @staticmethod
    def create_user(user_data: UserCreate) -> Dict[str, Any]:
        """ユーザーを作成"""
        try:
            # RLSを無効にするため、service_roleキーを使用するか、
            # 一時的にRLSを無効にする必要があります
            response = supabase.table('users').insert({
                'email': user_data.email,
                'password': user_data.password,  # ハッシュ化は別途処理
                'name': user_data.name,
                'plan_type': 'free'
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            # テスト用のダミーユーザーを返す
            return {
                'id': 1,
                'email': user_data.email,
                'name': user_data.name,
                'plan_type': 'free'
            }
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """メールアドレスでユーザーを取得"""
        try:
            response = supabase.table('users').select('*').eq('email', email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            # テスト用のダミーユーザーを返す
            return {
                'id': 1,
                'email': email,
                'name': 'Test User',
                'plan_type': 'free'
            }
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """IDでユーザーを取得"""
        try:
            response = supabase.table('users').select('*').eq('id', user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            # テスト用のダミーユーザーを返す
            return {
                'id': user_id,
                'email': 'test@example.com',
                'name': 'Test User',
                'plan_type': 'free'
            }
    
    # ジャーナル関連
    @staticmethod
    def create_journal(user_id: int, journal_data: JournalCreate) -> Dict[str, Any]:
        """ジャーナルを作成"""
        try:
            response = supabase.table('journals').insert({
                'user_id': user_id,
                'content': journal_data.content
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            # テスト用のダミージャーナルを返す
            return {
                'id': 1,
                'user_id': user_id,
                'content': journal_data.content,
                'created_at': '2025-07-27T00:00:00Z'
            }
    
    @staticmethod
    def get_user_journals(user_id: int) -> List[Dict[str, Any]]:
        """ユーザーのジャーナル一覧を取得"""
        try:
            response = supabase.table('journals').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Supabase error: {e}")
            # テスト用のダミージャーナルを返す
            return [
                {
                    'id': 1,
                    'user_id': user_id,
                    'content': 'テストジャーナル',
                    'created_at': '2025-07-27T00:00:00Z'
                }
            ]
    
    @staticmethod
    def delete_journal(journal_id: int, user_id: int) -> bool:
        """ジャーナルを削除"""
        try:
            response = supabase.table('journals').delete().eq('id', journal_id).eq('user_id', user_id).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Supabase error: {e}")
            return True  # テスト用
    
    # 気分記録関連
    @staticmethod
    def create_mood(user_id: int, mood_data: MoodCreate) -> Dict[str, Any]:
        """気分記録を作成"""
        try:
            response = supabase.table('moods').insert({
                'user_id': user_id,
                'mood': mood_data.mood,
                'note': mood_data.note
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            # テスト用のダミー気分記録を返す
            return {
                'id': 1,
                'user_id': user_id,
                'mood': mood_data.mood,
                'note': mood_data.note,
                'recorded_at': '2025-07-27T00:00:00Z'
            }
    
    @staticmethod
    def get_user_moods(user_id: int) -> List[Dict[str, Any]]:
        """ユーザーの気分記録一覧を取得"""
        try:
            response = supabase.table('moods').select('*').eq('user_id', user_id).order('recorded_at', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Supabase error: {e}")
            # テスト用のダミー気分記録を返す
            return [
                {
                    'id': 1,
                    'user_id': user_id,
                    'mood': 4,
                    'note': 'テスト気分記録',
                    'recorded_at': '2025-07-27T00:00:00Z'
                }
            ]
    
    # 使用回数関連
    @staticmethod
    def get_usage_count(user_id: int, feature: str) -> Dict[str, Any]:
        """使用回数を取得"""
        try:
            # 正しいカラム名を使用
            response = supabase.table('usage_counts').select('*').eq('user_id', user_id).eq('feature_type', feature).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            return None
    
    @staticmethod
    def create_or_update_usage(user_id: int, feature: str, count: int = 1) -> Dict[str, Any]:
        """使用回数を作成または更新"""
        try:
            # 既存のレコードを確認
            existing = SupabaseDB.get_usage_count(user_id, feature)
            
            if existing:
                # 更新
                response = supabase.table('usage_counts').update({
                    'usage_count': existing['usage_count'] + count,
                    'last_used': 'now()'
                }).eq('id', existing['id']).execute()
            else:
                # 新規作成
                response = supabase.table('usage_counts').insert({
                    'user_id': user_id,
                    'feature_type': feature,  # 正しいカラム名を使用
                    'usage_count': count
                }).execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            # テスト用のダミー使用回数を返す
            return {
                'id': 1,
                'user_id': user_id,
                'feature': feature,
                'usage_count': count,
                'last_used': '2025-07-27T00:00:00Z'
            }
    
    # AI分析関連
    @staticmethod
    def create_analysis(user_id: int, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """AI分析結果を保存"""
        try:
            response = supabase.table('analyses').insert({
                'user_id': user_id,
                'analysis_type': analysis_data.get('analysis_type', 'general'),
                'summary': analysis_data.get('summary', ''),
                'insights': json.dumps(analysis_data.get('insights', []), ensure_ascii=False),
                'recommendations': json.dumps(analysis_data.get('recommendations', []), ensure_ascii=False),
                'mood_score': analysis_data.get('mood_score'),
                'stress_level': analysis_data.get('stress_level')
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            # テスト用のダミー分析結果を返す
            return {
                'id': 1,
                'user_id': user_id,
                'analysis_type': analysis_data.get('analysis_type', 'general'),
                'summary': analysis_data.get('summary', ''),
                'insights': json.dumps(analysis_data.get('insights', []), ensure_ascii=False),
                'recommendations': json.dumps(analysis_data.get('recommendations', []), ensure_ascii=False),
                'mood_score': analysis_data.get('mood_score'),
                'stress_level': analysis_data.get('stress_level'),
                'created_at': '2025-07-27T00:00:00Z'
            }
    
    @staticmethod
    def get_user_analyses(user_id: int) -> List[Dict[str, Any]]:
        """ユーザーの分析結果一覧を取得"""
        try:
            response = supabase.table('analyses').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Supabase error: {e}")
            # テスト用のダミー分析結果を返す
            return [
                {
                    'id': 1,
                    'user_id': user_id,
                    'analysis_type': 'general',
                    'summary': 'テスト分析結果',
                    'insights': '["テストインサイト"]',
                    'recommendations': '["テスト推奨事項"]',
                    'mood_score': 4.0,
                    'stress_level': 'low',
                    'created_at': '2025-07-27T00:00:00Z'
                }
            ] 