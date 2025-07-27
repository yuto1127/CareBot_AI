import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random
from app.database.supabase_db import SupabaseDB

class PomodoroTimer:
    """ポモドーロタイマーシステム"""
    
    def __init__(self):
        # デフォルト設定
        self.default_settings = {
            "focus_duration": 1500,    # 25分
            "break_duration": 300,     # 5分
            "long_break_duration": 900, # 15分
            "cycles_before_long_break": 4,
            "auto_start_breaks": False,
            "auto_start_focus": False,
            "sound_enabled": True
        }
        
        # セッション状態
        self.session_states = {
            "idle": "idle",           # 待機中
            "focus": "focus",         # 集中中
            "break": "break",         # 休憩中
            "long_break": "long_break", # 長い休憩中
            "paused": "paused"        # 一時停止中
        }
    
    def create_session(self, user_id: int, settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """ポモドーロセッションを作成"""
        if settings is None:
            settings = self.default_settings.copy()
        
        session_data = {
            "session_id": f"pomodoro_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "user_id": user_id,
            "settings": settings,
            "current_state": self.session_states["idle"],
            "current_cycle": 0,
            "total_cycles": 0,
            "total_focus_time": 0,
            "total_break_time": 0,
            "start_time": None,
            "end_time": None,
            "pause_time": None,
            "resume_time": None,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        return session_data
    
    def start_focus_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """集中セッションを開始"""
        session_data["current_state"] = self.session_states["focus"]
        session_data["current_cycle"] += 1
        session_data["start_time"] = datetime.now().isoformat()
        session_data["pause_time"] = None
        session_data["resume_time"] = None
        
        return session_data
    
    def start_break_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """休憩セッションを開始"""
        # 長い休憩かどうかを判定
        if session_data["current_cycle"] % session_data["settings"]["cycles_before_long_break"] == 0:
            session_data["current_state"] = self.session_states["long_break"]
        else:
            session_data["current_state"] = self.session_states["break"]
        
        session_data["start_time"] = datetime.now().isoformat()
        session_data["pause_time"] = None
        session_data["resume_time"] = None
        
        return session_data
    
    def pause_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """セッションを一時停止"""
        if session_data["current_state"] in [self.session_states["focus"], self.session_states["break"], self.session_states["long_break"]]:
            session_data["current_state"] = self.session_states["paused"]
            session_data["pause_time"] = datetime.now().isoformat()
        
        return session_data
    
    def resume_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """セッションを再開"""
        if session_data["current_state"] == self.session_states["paused"]:
            # 元の状態に戻す
            if session_data["current_cycle"] % session_data["settings"]["cycles_before_long_break"] == 0:
                session_data["current_state"] = self.session_states["long_break"]
            elif session_data["current_cycle"] % 2 == 1:  # 奇数サイクルは休憩
                session_data["current_state"] = self.session_states["break"]
            else:
                session_data["current_state"] = self.session_states["focus"]
            
            session_data["resume_time"] = datetime.now().isoformat()
        
        return session_data
    
    def complete_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """セッションを完了"""
        session_data["end_time"] = datetime.now().isoformat()
        session_data["status"] = "completed"
        
        # 統計を計算
        session_data = self._calculate_session_stats(session_data)
        
        # セッション記録を保存
        self._save_session_record(session_data)
        
        return session_data
    
    def get_session_progress(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """セッションの進行状況を取得"""
        if not session_data["start_time"]:
            return {
                "state": session_data["current_state"],
                "cycle": session_data["current_cycle"],
                "elapsed_time": 0,
                "remaining_time": 0,
                "progress_percentage": 0
            }
        
        start_time = datetime.fromisoformat(session_data["start_time"])
        current_time = datetime.now()
        
        # 一時停止時間を考慮
        pause_duration = 0
        if session_data["pause_time"] and session_data["resume_time"]:
            pause_start = datetime.fromisoformat(session_data["pause_time"])
            pause_end = datetime.fromisoformat(session_data["resume_time"])
            pause_duration = (pause_end - pause_start).total_seconds()
        elif session_data["pause_time"] and not session_data["resume_time"]:
            pause_start = datetime.fromisoformat(session_data["pause_time"])
            pause_duration = (current_time - pause_start).total_seconds()
        
        elapsed_time = (current_time - start_time).total_seconds() - pause_duration
        
        # 現在のセッションの目標時間を取得
        if session_data["current_state"] == self.session_states["focus"]:
            target_duration = session_data["settings"]["focus_duration"]
        elif session_data["current_state"] == self.session_states["long_break"]:
            target_duration = session_data["settings"]["long_break_duration"]
        else:
            target_duration = session_data["settings"]["break_duration"]
        
        remaining_time = max(0, target_duration - elapsed_time)
        progress_percentage = min(100, (elapsed_time / target_duration) * 100) if target_duration > 0 else 0
        
        return {
            "state": session_data["current_state"],
            "cycle": session_data["current_cycle"],
            "elapsed_time": int(elapsed_time),
            "remaining_time": int(remaining_time),
            "progress_percentage": round(progress_percentage, 1),
            "target_duration": target_duration
        }
    
    def _calculate_session_stats(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """セッション統計を計算"""
        if not session_data["start_time"] or not session_data["end_time"]:
            return session_data
        
        start_time = datetime.fromisoformat(session_data["start_time"])
        end_time = datetime.fromisoformat(session_data["end_time"])
        
        # 一時停止時間を考慮
        pause_duration = 0
        if session_data["pause_time"] and session_data["resume_time"]:
            pause_start = datetime.fromisoformat(session_data["pause_time"])
            pause_end = datetime.fromisoformat(session_data["resume_time"])
            pause_duration = (pause_end - pause_start).total_seconds()
        
        total_duration = (end_time - start_time).total_seconds() - pause_duration
        
        # 集中時間と休憩時間を推定
        focus_cycles = (session_data["current_cycle"] + 1) // 2
        break_cycles = session_data["current_cycle"] // 2
        
        estimated_focus_time = focus_cycles * session_data["settings"]["focus_duration"]
        estimated_break_time = break_cycles * session_data["settings"]["break_duration"]
        
        session_data["total_focus_time"] = int(estimated_focus_time)
        session_data["total_break_time"] = int(estimated_break_time)
        session_data["total_duration"] = int(total_duration)
        
        return session_data
    
    def _save_session_record(self, session_data: Dict[str, Any]) -> bool:
        """セッション記録を保存"""
        try:
            # ジャーナルとして保存
            journal_data = {
                "user_id": session_data["user_id"],
                "title": f"ポモドーロセッション - {session_data['current_cycle']}サイクル完了",
                "content": f"ポモドーロセッションを完了しました。\n\n完了サイクル: {session_data['current_cycle']}回\n総集中時間: {session_data.get('total_focus_time', 0)}秒\n総休憩時間: {session_data.get('total_break_time', 0)}秒\n総時間: {session_data.get('total_duration', 0)}秒\n開始時間: {session_data['start_time']}\n終了時間: {session_data['end_time']}",
                "session_type": "pomodoro",
                "session_id": session_data["session_id"]
            }
            
            SupabaseDB.create_journal(journal_data)
            return True
            
        except Exception as e:
            print(f"セッション記録保存エラー: {e}")
            return False
    
    def get_user_statistics(self, user_id: int) -> Dict[str, Any]:
        """ユーザーのポモドーロ統計を取得"""
        try:
            # ポモドーロセッションをジャーナルから取得
            journals = SupabaseDB.get_user_journals(user_id)
            pomodoro_sessions = [
                journal for journal in journals 
                if journal.get('session_type') == 'pomodoro'
            ]
            
            # 統計を計算
            total_sessions = len(pomodoro_sessions)
            total_focus_time = 0
            total_break_time = 0
            total_cycles = 0
            
            for session in pomodoro_sessions:
                # セッション内容から統計を抽出（簡易版）
                content = session.get('content', '')
                if '総集中時間:' in content:
                    try:
                        focus_time = int(content.split('総集中時間:')[1].split('秒')[0].strip())
                        total_focus_time += focus_time
                    except:
                        pass
                
                if '完了サイクル:' in content:
                    try:
                        cycles = int(content.split('完了サイクル:')[1].split('回')[0].strip())
                        total_cycles += cycles
                    except:
                        pass
            
            return {
                "total_sessions": total_sessions,
                "total_focus_time": total_focus_time,
                "total_break_time": total_break_time,
                "total_cycles": total_cycles,
                "average_focus_time_per_session": total_focus_time // total_sessions if total_sessions > 0 else 0,
                "average_cycles_per_session": total_cycles // total_sessions if total_sessions > 0 else 0
            }
            
        except Exception as e:
            print(f"統計取得エラー: {e}")
            return {
                "total_sessions": 0,
                "total_focus_time": 0,
                "total_break_time": 0,
                "total_cycles": 0,
                "average_focus_time_per_session": 0,
                "average_cycles_per_session": 0
            } 