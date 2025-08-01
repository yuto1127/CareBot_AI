from typing import List, Dict, Any, Optional
from app.config.supabase import supabase, supabase_admin
from app.schemas.user import UserCreate, UserResponse
from app.schemas.journal import JournalCreate, JournalResponse
from app.schemas.mood import MoodCreate, MoodResponse
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
import json
import logging
from datetime import datetime
import bcrypt
from app.utils.logger import logger
import os

logger = logging.getLogger(__name__)

class SupabaseDB:
    """Supabaseデータベース操作クラス"""
    
    # ユーザー関連
    @staticmethod
    def create_user(user_data) -> Dict[str, Any]:
        """ユーザーを作成"""
        try:
            logger.info(f"=== ユーザー作成開始 ===")
            logger.info(f"メールアドレス: {user_data.email}")
            logger.info(f"ユーザー名: {getattr(user_data, 'name', getattr(user_data, 'username', 'Unknown'))}")
            
            # パスワードをハッシュ化
            hashed_password = bcrypt.hashpw(
                user_data.password.encode('utf-8'), 
                bcrypt.gensalt()
            ).decode('utf-8')
            
            logger.info("パスワードハッシュ化完了")
            
            # Supabaseに挿入するデータ
            insert_data = {
                'email': user_data.email,
                'password': hashed_password,
                'name': getattr(user_data, 'name', getattr(user_data, 'username', 'Unknown')),
                'plan_type': getattr(user_data, 'plan_type', 'free')
            }
            
            logger.info(f"Supabaseに挿入するデータ: {insert_data}")
            print(f"DEBUG: Supabase挿入データ - {insert_data}")
            
            # service_roleキーを使用してRLSをバイパス
            logger.info("Supabaseテーブルに挿入中（service_role使用）...")
            response = supabase_admin.table('users').insert(insert_data).execute()
            
            logger.info(f"Supabaseレスポンス: {response}")
            print(f"DEBUG: Supabaseレスポンス - {response}")
            
            if response.data:
                user = response.data[0]
                logger.info(f"Supabase挿入成功: {user}")
                print(f"DEBUG: Supabase挿入成功 - {user}")
                
                # パスワードをレスポンスから除外
                user.pop('password', None)
                logger.info(f"ユーザー作成成功: {user['email']}")
                return user
            else:
                logger.error("Supabase挿入失敗: レスポンスデータなし")
                print(f"DEBUG: Supabase挿入失敗 - レスポンスデータなし")
                return None
                
        except Exception as e:
            logger.error(f"ユーザー作成エラー: {e}")
            print(f"DEBUG: ユーザー作成エラー - {e}")
            print(f"DEBUG: エラータイプ - {type(e)}")
            raise
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """メールアドレスでユーザーを取得"""
        try:
            response = supabase_admin.table('users').select('*').eq('email', email).execute()
                
            if response.data:
                user = response.data[0]
                logger.info(f"ユーザー取得成功: {email}")
                return user
            else:
                logger.info(f"ユーザーが見つかりません: {email}")
                return None
                
        except Exception as e:
            logger.error(f"ユーザー取得エラー: {e}")
            return None

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """IDでユーザーを取得"""
        try:
            response = supabase_admin.table('users').select('*').eq('id', user_id).execute()
                
            if response.data:
                user = response.data[0]
                # パスワードをレスポンスから除外
                user.pop('password', None)
                logger.info(f"ユーザー取得成功: ID {user_id}")
                return user
            else:
                logger.info(f"ユーザーが見つかりません: ID {user_id}")
                return None
                
        except Exception as e:
            logger.error(f"ユーザー取得エラー: {e}")
            return None

    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
        """ユーザー認証"""
        try:
            logger.info(f"認証開始: {email}")
            print(f"DEBUG: 認証開始 - email: {email}")
            
            # メールアドレスでユーザーを検索
            user = SupabaseDB.get_user_by_email(email)
            print(f"DEBUG: ユーザー検索結果 - user exists: {user is not None}")
            
            if not user:
                logger.warning(f"ユーザーが見つかりません: {email}")
                print(f"DEBUG: ユーザーが見つかりません: {email}")
                return None
            
            print(f"DEBUG: ユーザー情報 - {user}")
            
            # パスワードフィールドが存在しない場合は認証失敗
            stored_password = user.get('password', '')
            print(f"DEBUG: パスワードフィールド存在 - {bool(stored_password)}")
            
            if not stored_password:
                logger.warning(f"パスワードフィールドが存在しません: {email}")
                print(f"DEBUG: パスワードフィールドが存在しません: {email}")
                return None
            
            # ハッシュ化されたパスワードを検証
            try:
                print(f"DEBUG: パスワード検証開始")
                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    logger.info(f"パスワード検証成功: {email}")
                    print(f"DEBUG: パスワード検証成功: {email}")
                    # パスワードをレスポンスから除外
                    user.pop('password', None)
                    return user
                else:
                    logger.warning(f"パスワード検証失敗: {email}")
                    print(f"DEBUG: パスワード検証失敗: {email}")
                    return None
            except Exception as e:
                logger.error(f"パスワード検証エラー: {e}")
                print(f"DEBUG: パスワード検証エラー: {e}")
                return None
                    
        except Exception as e:
            logger.error(f"認証エラー: {e}")
            print(f"DEBUG: 認証エラー: {e}")
            return None
    
    # ジャーナル関連
    @staticmethod
    def create_journal(user_id: int, journal_data: JournalCreate) -> Dict[str, Any]:
        """ジャーナルを作成"""
        try:
            response = supabase_admin.table('journals').insert({
                'user_id': user_id,
                'content': journal_data.content
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"ジャーナル作成エラー: {e}")
            raise
    
    @staticmethod
    def get_user_journals(user_id: int) -> List[Dict[str, Any]]:
        """ユーザーのジャーナル一覧を取得"""
        try:
            response = supabase_admin.table('journals').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
            return response.data
        except Exception as e:
            logger.error(f"ジャーナル取得エラー: {e}")
            raise
    
    @staticmethod
    def delete_journal(journal_id: int, user_id: int) -> bool:
        """ジャーナルを削除"""
        try:
            response = supabase_admin.table('journals').delete().eq('id', journal_id).eq('user_id', user_id).execute()
            return len(response.data) > 0
        except Exception as e:
            logger.error(f"ジャーナル削除エラー: {e}")
            raise
    
    # 気分記録関連
    @staticmethod
    def create_mood(user_id: int, mood_data: MoodCreate) -> Dict[str, Any]:
        """気分記録を作成"""
        try:
            response = supabase_admin.table('moods').insert({
                'user_id': user_id,
                'mood': mood_data.mood,
                'note': mood_data.note
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"気分記録作成エラー: {e}")
            raise
    
    @staticmethod
    def get_user_moods(user_id: int) -> List[Dict[str, Any]]:
        """ユーザーの気分記録一覧を取得"""
        try:
            response = supabase_admin.table('moods').select('*').eq('user_id', user_id).order('recorded_at', desc=True).execute()
            return response.data
        except Exception as e:
            logger.error(f"気分記録取得エラー: {e}")
            raise
    
    @staticmethod
    def delete_mood(mood_id: int, user_id: int) -> bool:
        """気分記録を削除"""
        try:
            response = supabase_admin.table('moods').delete().eq('id', mood_id).eq('user_id', user_id).execute()
            deleted_count = len(response.data) if response.data else 0
            logger.info(f"気分記録削除: ID {mood_id}, 削除件数: {deleted_count}")
            return deleted_count > 0
        except Exception as e:
            logger.error(f"気分記録削除エラー: {e}")
            raise
    
    # 使用回数関連
    @staticmethod
    def get_usage_count(user_id: int, feature: str) -> Dict[str, Any]:
        """使用回数を取得"""
        try:
            response = supabase_admin.table('usage_counts').select('*').eq('user_id', user_id).eq('feature_type', feature).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"使用回数取得エラー: {e}")
            raise
    
    @staticmethod
    def create_or_update_usage(user_id: int, feature: str, count: int = 1) -> Dict[str, Any]:
        """使用回数を作成または更新"""
        try:
            # 既存のレコードを確認
            existing = SupabaseDB.get_usage_count(user_id, feature)
            
            if existing:
                # 更新
                response = supabase_admin.table('usage_counts').update({
                    'usage_count': existing['usage_count'] + count,
                    'last_used': 'now()'
                }).eq('id', existing['id']).execute()
            else:
                # 新規作成
                response = supabase_admin.table('usage_counts').insert({
                    'user_id': user_id,
                    'feature_type': feature,
                    'usage_count': count
                }).execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"使用回数更新エラー: {e}")
            raise
    
    # AI分析関連
    @staticmethod
    def create_analysis(user_id: int, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """AI分析結果を作成"""
        try:
            response = supabase_admin.table('analyses').insert({
                'user_id': user_id,
                'analysis_type': analysis_data.get('analysis_type', 'general'),
                'summary': analysis_data.get('summary', ''),
                'insights': json.dumps(analysis_data.get('insights', [])),
                'recommendations': json.dumps(analysis_data.get('recommendations', [])),
                'mood_score': analysis_data.get('mood_score', 0),
                'stress_level': analysis_data.get('stress_level', 'unknown')
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"分析結果作成エラー: {e}")
            raise
    
    @staticmethod
    def get_user_analyses(user_id: int) -> List[Dict[str, Any]]:
        """ユーザーの分析結果一覧を取得"""
        try:
            response = supabase_admin.table('analyses').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
            return response.data
        except Exception as e:
            logger.error(f"分析結果取得エラー: {e}")
            raise

    def get_table_structure(self, table_name: str) -> Dict[str, Any]:
        """テーブル構造を取得"""
        try:
            # テーブルのカラム情報を取得
            result = supabase_admin.table(table_name).select("*").limit(1).execute()
            
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
            journals_result = supabase_admin.table('journals').select('id').eq('user_id', user_id).execute()
            stats['total_journals'] = len(journals_result.data) if journals_result.data else 0
            
            # 気分記録数
            moods_result = supabase_admin.table('moods').select('id, mood').eq('user_id', user_id).execute()
            if moods_result.data:
                stats['total_moods'] = len(moods_result.data)
                # 平均気分スコアを計算
                mood_scores = [mood['mood'] for mood in moods_result.data if mood.get('mood') is not None]
                if mood_scores:
                    stats['average_mood_score'] = sum(mood_scores) / len(mood_scores)
            
            # CBTセッション数（ジャーナルから推定）
            cbt_journals = [j for j in journals_result.data if j.get('content', '').find('CBT') != -1]
            stats['total_cbt_sessions'] = len(cbt_journals)
            
            # 最後のアクティビティを取得
            all_activities = []
            
            # ジャーナルの最後の更新
            if journals_result.data:
                latest_journal = max(journals_result.data, key=lambda x: x.get('created_at', ''))
                all_activities.append(('journal', latest_journal.get('created_at')))
            
            # 気分記録の最後の更新
            if moods_result.data:
                latest_mood = max(moods_result.data, key=lambda x: x.get('recorded_at', ''))
                all_activities.append(('mood', latest_mood.get('recorded_at')))
            
            if all_activities:
                latest_activity = max(all_activities, key=lambda x: x[1])
                stats['last_activity'] = {
                    'type': latest_activity[0],
                    'date': latest_activity[1]
                }
            
            return stats
            
        except Exception as e:
            logger.error(f"ユーザー統計取得エラー: {e}")
            raise
    
    def update_user(self, user_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """ユーザー情報を更新"""
        try:
            response = supabase_admin.table('users').update(update_data).eq('id', user_id).execute()
            if response.data:
                user = response.data[0]
                # パスワードをレスポンスから除外
                user.pop('password', None)
                return user
            return None
        except Exception as e:
            logger.error(f"ユーザー更新エラー: {e}")
            raise
    
    def delete_user(self, user_id: int) -> bool:
        """ユーザーを削除"""
        try:
            response = supabase_admin.table('users').delete().eq('id', user_id).execute()
            return len(response.data) > 0
        except Exception as e:
            logger.error(f"ユーザー削除エラー: {e}")
            raise 
    
    # プロフィール関連
    @staticmethod
    def get_user_profile(user_id: int) -> Optional[Dict[str, Any]]:
        """ユーザーのプロフィールを取得"""
        try:
            response = supabase_admin.table('profiles').select('*').eq('user_id', user_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"プロフィール取得エラー: {e}")
            raise
    
    @staticmethod
    def create_user_profile(user_id: int, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """ユーザープロフィールを作成"""
        try:
            response = supabase_admin.table('profiles').insert({
                'user_id': user_id,
                'avatar_url': profile_data.get('avatar_url'),
                'bio': profile_data.get('bio'),
                'preferences': profile_data.get('preferences', {})
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"プロフィール作成エラー: {e}")
            raise
    
    @staticmethod
    def update_user_profile(user_id: int, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """ユーザープロフィールを更新"""
        try:
            response = supabase_admin.table('profiles').update(profile_data).eq('user_id', user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"プロフィール更新エラー: {e}")
            raise
    
    # 機能制限関連
    @staticmethod
    def get_feature_limits() -> List[Dict[str, Any]]:
        """機能制限一覧を取得"""
        try:
            response = supabase_admin.table('feature_limits').select('*').execute()
            return response.data
        except Exception as e:
            logger.error(f"機能制限取得エラー: {e}")
            raise
    
    @staticmethod
    def get_feature_limit(feature_name: str) -> Optional[Dict[str, Any]]:
        """特定の機能制限を取得"""
        try:
            response = supabase_admin.table('feature_limits').select('*').eq('feature_name', feature_name).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"機能制限取得エラー: {e}")
            raise
    
    @staticmethod
    def check_user_feature_access(user_id: int, feature_name: str) -> Dict[str, Any]:
        """ユーザーの機能アクセス権限をチェック"""
        try:
            # ユーザーのプランタイプを取得
            user = SupabaseDB.get_user_by_id(user_id)
            if not user:
                return {"can_access": False, "reason": "User not found"}
            
            plan_type = user.get('plan_type', 'free')
            
            # 機能制限を取得
            feature_limit = SupabaseDB.get_feature_limit(feature_name)
            if not feature_limit:
                return {"can_access": True, "reason": "No limits set"}
            
            # 現在の使用回数を取得
            usage = SupabaseDB.get_usage_count(user_id, feature_name)
            current_usage = usage.get('usage_count', 0) if usage else 0
            
            # プランに応じた制限を取得
            if plan_type == 'premium':
                limit = feature_limit.get('premium_limit', 100)
            else:
                limit = feature_limit.get('free_limit', 10)
            
            can_access = current_usage < limit
            
            return {
                "can_access": can_access,
                "current_usage": current_usage,
                "limit": limit,
                "plan_type": plan_type,
                "feature_name": feature_name
            }
            
        except Exception as e:
            logger.error(f"機能アクセスチェックエラー: {e}")
            raise 
    
    # 管理者機能
    @staticmethod
    def get_all_users() -> List[Dict[str, Any]]:
        """すべてのユーザーを取得（管理者用）"""
        try:
            response = supabase_admin.table('users').select('*').execute()
            return response.data
        except Exception as e:
            logger.error(f"全ユーザー取得エラー: {e}")
            raise
    
    @staticmethod
    def update_user_role(user_id: int, role: str, updated_by: int, reason: str = "") -> Optional[Dict[str, Any]]:
        """ユーザーのロールを更新（管理者用）"""
        try:
            # ロール更新
            update_data = {
                'role': role,
                'updated_at': datetime.now().isoformat()
            }
            
            response = supabase_admin.table('users').update(update_data).eq('id', user_id).execute()
            
            if response.data:
                # ロール変更履歴を記録（オプション）
                logger.info(f"ロール更新: ユーザーID {user_id} -> {role} (更新者: {updated_by}, 理由: {reason})")
                return response.data[0]
            return None
            
        except Exception as e:
            logger.error(f"ロール更新エラー: {e}")
            raise
    
    @staticmethod
    def get_user_by_role(role: str) -> List[Dict[str, Any]]:
        """特定のロールを持つユーザーを取得"""
        try:
            response = supabase_admin.table('users').select('*').eq('role', role).execute()
            return response.data
        except Exception as e:
            logger.error(f"ロール別ユーザー取得エラー: {e}")
            raise
    
    @staticmethod
    def get_user_stats_by_role(role: str) -> Dict[str, Any]:
        """特定のロールを持つユーザーの統計を取得"""
        try:
            users = SupabaseDB.get_user_by_role(role)
            
            stats = {
                'role': role,
                'total_users': len(users),
                'active_users': len([u for u in users if u.get('last_login')]),
                'premium_users': len([u for u in users if u.get('plan_type') == 'premium']),
                'free_users': len([u for u in users if u.get('plan_type') == 'free'])
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"ロール別統計取得エラー: {e}")
            raise 