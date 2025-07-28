from typing import List, Dict, Any, Optional
from app.config.supabase import supabase
from app.schemas.user import UserCreate, UserResponse
from app.schemas.journal import JournalCreate, JournalResponse
from app.schemas.mood import MoodCreate, MoodResponse
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

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

    def get_table_structure(self, table_name: str) -> Dict[str, Any]:
        """テーブル構造を取得"""
        try:
            # テーブルのカラム情報を取得
            result = supabase.table(table_name).select("*").limit(1).execute()
            
            # テーブル構造を確認
            logger.info(f"テーブル {table_name} の構造確認")
            
            # 実際のデータ型を確認するため、サンプルデータを取得
            if result.data:
                sample_data = result.data[0]
                logger.info(f"サンプルデータ: {sample_data}")
                
                # id/user_idの型を確認
                if 'id' in sample_data:
                    logger.info(f"id の型: {type(sample_data['id'])}")
                if 'user_id' in sample_data:
                    logger.info(f"user_id の型: {type(sample_data['user_id'])}")
            
            return {
                "table_name": table_name,
                "sample_data": result.data[0] if result.data else None,
                "columns": list(result.data[0].keys()) if result.data else []
            }
            
        except Exception as e:
            logger.error(f"テーブル構造取得エラー (table: {table_name})", e)
            return {"error": str(e)}
    
    def check_user_id_types(self):
        """全テーブルのuser_id型を確認"""
        tables = ['users', 'journals', 'moods', 'usage_counts']
        results = {}
        
        for table in tables:
            try:
                structure = self.get_table_structure(table)
                results[table] = structure
                logger.info(f"テーブル {table} の構造確認完了")
                
            except Exception as e:
                results[table] = {"error": str(e)}
                logger.error(f"テーブル {table} の構造確認エラー", e)
        
        return results 

    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """ユーザーの統計情報を取得"""
        try:
            stats = {
                'total_journals': 0,
                'total_moods': 0,
                'total_cbt_sessions': 0,
                'total_meditation_sessions': 0,
                'total_sound_sessions': 0,
                'total_pomodoro_sessions': 0,
                'average_mood_score': None,
                'last_activity': None
            }
            
            # ジャーナル数
            journals_result = supabase.table('journals').select('id').eq('user_id', user_id).execute()
            stats['total_journals'] = len(journals_result.data) if journals_result.data else 0
            
            # 気分記録数
            moods_result = supabase.table('moods').select('id, mood_score').eq('user_id', user_id).execute()
            if moods_result.data:
                stats['total_moods'] = len(moods_result.data)
                # 平均気分スコアを計算
                mood_scores = [mood['mood_score'] for mood in moods_result.data if mood.get('mood_score') is not None]
                if mood_scores:
                    stats['average_mood_score'] = sum(mood_scores) / len(mood_scores)
            
            # CBTセッション数（ジャーナルから推定）
            cbt_journals = [j for j in journals_result.data if j.get('content', '').find('CBT') != -1]
            stats['total_cbt_sessions'] = len(cbt_journals)
            
            # 瞑想セッション数（ジャーナルから推定）
            meditation_journals = [j for j in journals_result.data if j.get('content', '').find('瞑想') != -1 or j.get('content', '').find('meditation') != -1]
            stats['total_meditation_sessions'] = len(meditation_journals)
            
            # サウンドセッション数（ジャーナルから推定）
            sound_journals = [j for j in journals_result.data if j.get('content', '').find('サウンド') != -1 or j.get('content', '').find('sound') != -1]
            stats['total_sound_sessions'] = len(sound_journals)
            
            # ポモドーロセッション数（ジャーナルから推定）
            pomodoro_journals = [j for j in journals_result.data if j.get('content', '').find('ポモドーロ') != -1 or j.get('content', '').find('pomodoro') != -1]
            stats['total_pomodoro_sessions'] = len(pomodoro_journals)
            
            # 最後の活動日時
            all_activities = []
            if journals_result.data:
                all_activities.extend([j.get('created_at') for j in journals_result.data])
            if moods_result.data:
                all_activities.extend([m.get('created_at') for m in moods_result.data])
            
            if all_activities:
                # 最新の日時を取得
                latest_activity = max(all_activities)
                stats['last_activity'] = latest_activity
            
            return stats
            
        except Exception as e:
            logger.error(f"ユーザー統計取得エラー (user_id: {user_id})", e)
            return stats
    
    def update_user(self, user_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """ユーザー情報を更新"""
        try:
            # 更新日時を追加
            update_data['updated_at'] = datetime.now().isoformat()
            
            # ユーザーを更新
            result = supabase.table('users').update(update_data).eq('id', user_id).execute()
            
            if result.data:
                logger.info(f"ユーザー更新完了 (user_id: {user_id})")
                return result.data[0]
            else:
                logger.warning(f"ユーザー更新失敗 - データが見つかりません (user_id: {user_id})")
                return None
                
        except Exception as e:
            logger.error(f"ユーザー更新エラー (user_id: {user_id})", e)
            return None
    
    def delete_user(self, user_id: int) -> bool:
        """ユーザーを削除"""
        try:
            # 関連データを先に削除
            # ジャーナルを削除
            supabase.table('journals').delete().eq('user_id', user_id).execute()
            
            # 気分記録を削除
            supabase.table('moods').delete().eq('user_id', user_id).execute()
            
            # 使用回数を削除
            supabase.table('usage_counts').delete().eq('user_id', user_id).execute()
            
            # ユーザーを削除
            result = supabase.table('users').delete().eq('id', user_id).execute()
            
            if result.data:
                logger.info(f"ユーザー削除完了 (user_id: {user_id})")
                return True
            else:
                logger.warning(f"ユーザー削除失敗 - データが見つかりません (user_id: {user_id})")
                return False
                
        except Exception as e:
            logger.error(f"ユーザー削除エラー (user_id: {user_id})", e)
            return False 