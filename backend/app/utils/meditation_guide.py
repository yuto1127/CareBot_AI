import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import random
from app.database.supabase_db import SupabaseDB

class MeditationGuide:
    """瞑想・マインドフルネスガイドシステム"""
    
    def __init__(self):
        # 瞑想セッションライブラリ
        self.meditation_sessions = {
            "breathing": {
                "id": "breathing_3min",
                "title": "3分間の呼吸瞑想",
                "duration": 180,  # 秒
                "audio_url": "/audio/meditation/breathing_3min.mp3",
                "description": "呼吸に集中して心を落ち着かせます",
                "category": "beginner",
                "tags": ["呼吸", "初心者", "短時間"]
            },
            "stress_relief": {
                "id": "stress_relief_10min",
                "title": "ストレス軽減のための10分間ガイド",
                "duration": 600,
                "audio_url": "/audio/meditation/stress_relief_10min.mp3",
                "description": "ストレスを感じる時のためのガイド",
                "category": "intermediate",
                "tags": ["ストレス", "リラックス", "中級"]
            },
            "sleep": {
                "id": "sleep_15min",
                "title": "睡眠のための15分間瞑想",
                "duration": 900,
                "audio_url": "/audio/meditation/sleep_15min.mp3",
                "description": "良質な睡眠のための瞑想",
                "category": "intermediate",
                "tags": ["睡眠", "リラックス", "夜"]
            },
            "focus": {
                "id": "focus_5min",
                "title": "集中力向上の5分間瞑想",
                "duration": 300,
                "audio_url": "/audio/meditation/focus_5min.mp3",
                "description": "仕事や勉強前の集中力向上",
                "category": "beginner",
                "tags": ["集中", "仕事", "短時間"]
            },
            "gratitude": {
                "id": "gratitude_7min",
                "title": "感謝の7分間瞑想",
                "duration": 420,
                "audio_url": "/audio/meditation/gratitude_7min.mp3",
                "description": "感謝の気持ちを深める瞑想",
                "category": "beginner",
                "tags": ["感謝", "ポジティブ", "初心者"]
            },
            "body_scan": {
                "id": "body_scan_12min",
                "title": "ボディスキャン12分間",
                "duration": 720,
                "audio_url": "/audio/meditation/body_scan_12min.mp3",
                "description": "体の各部分に意識を向ける瞑想",
                "category": "intermediate",
                "tags": ["ボディスキャン", "リラックス", "中級"]
            }
        }
        
        # カテゴリ別推奨
        self.category_recommendations = {
            "beginner": ["breathing", "focus", "gratitude"],
            "intermediate": ["stress_relief", "sleep", "body_scan"],
            "advanced": ["stress_relief", "body_scan"]
        }
        
        # 時間別推奨
        self.time_recommendations = {
            "morning": ["focus", "gratitude"],
            "afternoon": ["breathing", "stress_relief"],
            "evening": ["sleep", "body_scan"]
        }
    
    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """すべての瞑想セッションを取得"""
        return list(self.meditation_sessions.values())
    
    def get_session_by_id(self, session_id: str) -> Optional[Dict[str, Any]]:
        """IDで瞑想セッションを取得"""
        return self.meditation_sessions.get(session_id)
    
    def get_sessions_by_category(self, category: str) -> List[Dict[str, Any]]:
        """カテゴリ別に瞑想セッションを取得"""
        return [
            session for session in self.meditation_sessions.values()
            if session["category"] == category
        ]
    
    def get_sessions_by_duration(self, max_duration: int) -> List[Dict[str, Any]]:
        """時間制限で瞑想セッションを取得"""
        return [
            session for session in self.meditation_sessions.values()
            if session["duration"] <= max_duration
        ]
    
    def get_personalized_recommendations(self, user_id: int, context: str = None) -> List[Dict[str, Any]]:
        """パーソナライズされた推奨セッションを取得"""
        try:
            # ユーザーの気分記録を取得
            moods = SupabaseDB.get_user_moods(user_id)
            if not moods:
                # 気分記録がない場合は初心者向けを推奨
                return [self.meditation_sessions[session_id] for session_id in self.category_recommendations["beginner"]]
            
            # 最新の気分を取得
            latest_mood = moods[0] if moods else None
            mood_score = latest_mood.get("mood", 3) if latest_mood else 3
            
            # 気分スコアに基づく推奨
            if mood_score <= 2:
                # 低い気分：ストレス軽減・睡眠向け
                recommended_ids = ["stress_relief", "sleep", "breathing"]
            elif mood_score <= 3:
                # 普通の気分：集中・感謝向け
                recommended_ids = ["focus", "gratitude", "breathing"]
            else:
                # 高い気分：感謝・集中向け
                recommended_ids = ["gratitude", "focus", "body_scan"]
            
            # コンテキストに基づく調整
            if context == "work":
                recommended_ids = ["focus"] + recommended_ids
            elif context == "sleep":
                recommended_ids = ["sleep"] + recommended_ids
            elif context == "stress":
                recommended_ids = ["stress_relief"] + recommended_ids
            
            # 重複を除去して返す
            seen_ids = set()
            recommendations = []
            for session_id in recommended_ids:
                if session_id not in seen_ids and session_id in self.meditation_sessions:
                    recommendations.append(self.meditation_sessions[session_id])
                    seen_ids.add(session_id)
            
            return recommendations[:3]  # 最大3つまで
            
        except Exception as e:
            print(f"推奨生成エラー: {e}")
            # エラー時は初心者向けを返す
            return [self.meditation_sessions[session_id] for session_id in self.category_recommendations["beginner"]]
    
    def start_meditation_session(self, user_id: int, session_id: str) -> Dict[str, Any]:
        """瞑想セッションを開始"""
        session = self.get_session_by_id(session_id)
        if not session:
            raise ValueError(f"瞑想セッション '{session_id}' が見つかりません")
        
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "start_time": datetime.now().isoformat(),
            "duration": session["duration"],
            "title": session["title"],
            "audio_url": session["audio_url"],
            "status": "active"
        }
        
        return session_data
    
    def complete_meditation_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """瞑想セッションを完了"""
        session_data["status"] = "completed"
        session_data["end_time"] = datetime.now().isoformat()
        session_data["actual_duration"] = self._calculate_actual_duration(
            session_data["start_time"], 
            session_data["end_time"]
        )
        
        # セッション記録を保存
        self._save_session_record(session_data)
        
        return session_data
    
    def _calculate_actual_duration(self, start_time: str, end_time: str) -> int:
        """実際のセッション時間を計算"""
        try:
            start = datetime.fromisoformat(start_time)
            end = datetime.fromisoformat(end_time)
            return int((end - start).total_seconds())
        except:
            return 0
    
    def _save_session_record(self, session_data: Dict[str, Any]) -> bool:
        """セッション記録を保存"""
        try:
            # ジャーナルとして保存
            journal_data = {
                "user_id": session_data["user_id"],
                "title": f"瞑想セッション - {session_data['title']}",
                "content": f"瞑想セッションを完了しました。\n\nセッション: {session_data['title']}\n予定時間: {session_data['duration']}秒\n実際の時間: {session_data.get('actual_duration', 0)}秒\n開始時間: {session_data['start_time']}\n終了時間: {session_data['end_time']}",
                "session_type": "meditation",
                "session_id": session_data["session_id"]
            }
            
            SupabaseDB.create_journal(journal_data)
            return True
            
        except Exception as e:
            print(f"セッション記録保存エラー: {e}")
            return False 