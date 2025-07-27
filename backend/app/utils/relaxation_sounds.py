import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import random
from app.database.supabase_db import SupabaseDB

class RelaxationSounds:
    """リラックスサウンドシステム"""
    
    def __init__(self):
        # サウンドライブラリ
        self.sounds = {
            "nature": {
                "rain": {
                    "id": "rain",
                    "name": "雨の音",
                    "category": "nature",
                    "audio_url": "/audio/sounds/rain.mp3",
                    "description": "静かな雨の音で心を落ち着かせます",
                    "tags": ["雨", "自然", "リラックス"],
                    "default_volume": 0.7
                },
                "waves": {
                    "id": "waves",
                    "name": "波の音",
                    "category": "nature",
                    "audio_url": "/audio/sounds/waves.mp3",
                    "description": "穏やかな波の音で海辺の雰囲気を演出",
                    "tags": ["海", "波", "自然"],
                    "default_volume": 0.6
                },
                "forest": {
                    "id": "forest",
                    "name": "森の音",
                    "category": "nature",
                    "audio_url": "/audio/sounds/forest.mp3",
                    "description": "鳥のさえずりと木々のざわめき",
                    "tags": ["森", "鳥", "自然"],
                    "default_volume": 0.5
                },
                "stream": {
                    "id": "stream",
                    "name": "小川の音",
                    "category": "nature",
                    "audio_url": "/audio/sounds/stream.mp3",
                    "description": "清らかな小川のせせらぎ",
                    "tags": ["川", "水", "自然"],
                    "default_volume": 0.6
                }
            },
            "ambient": {
                "white_noise": {
                    "id": "white_noise",
                    "name": "ホワイトノイズ",
                    "category": "ambient",
                    "audio_url": "/audio/sounds/white_noise.mp3",
                    "description": "集中力を高めるホワイトノイズ",
                    "tags": ["集中", "ノイズ", "作業"],
                    "default_volume": 0.4
                },
                "pink_noise": {
                    "id": "pink_noise",
                    "name": "ピンクノイズ",
                    "category": "ambient",
                    "audio_url": "/audio/sounds/pink_noise.mp3",
                    "description": "リラックス効果のあるピンクノイズ",
                    "tags": ["リラックス", "ノイズ", "睡眠"],
                    "default_volume": 0.3
                },
                "brown_noise": {
                    "id": "brown_noise",
                    "name": "ブラウンノイズ",
                    "category": "ambient",
                    "audio_url": "/audio/sounds/brown_noise.mp3",
                    "description": "深いリラックス効果のあるブラウンノイズ",
                    "tags": ["リラックス", "ノイズ", "深い睡眠"],
                    "default_volume": 0.3
                }
            },
            "instruments": {
                "piano": {
                    "id": "piano",
                    "name": "ピアノ",
                    "category": "instruments",
                    "audio_url": "/audio/sounds/piano.mp3",
                    "description": "優雅なピアノの調べ",
                    "tags": ["ピアノ", "音楽", "優雅"],
                    "default_volume": 0.5
                },
                "flute": {
                    "id": "flute",
                    "name": "フルート",
                    "category": "instruments",
                    "audio_url": "/audio/sounds/flute.mp3",
                    "description": "癒しのフルートの音色",
                    "tags": ["フルート", "音楽", "癒し"],
                    "default_volume": 0.4
                },
                "strings": {
                    "id": "strings",
                    "name": "弦楽器",
                    "category": "instruments",
                    "audio_url": "/audio/sounds/strings.mp3",
                    "description": "美しい弦楽器のハーモニー",
                    "tags": ["弦楽器", "音楽", "美しい"],
                    "default_volume": 0.5
                }
            }
        }
        
        # プリセットサウンドスケープ
        self.presets = {
            "sleep": {
                "name": "睡眠用",
                "description": "良質な睡眠のためのサウンドスケープ",
                "sounds": [
                    {"id": "rain", "volume": 0.4},
                    {"id": "pink_noise", "volume": 0.2}
                ]
            },
            "focus": {
                "name": "集中用",
                "description": "作業や勉強に集中するためのサウンドスケープ",
                "sounds": [
                    {"id": "white_noise", "volume": 0.5},
                    {"id": "forest", "volume": 0.3}
                ]
            },
            "relaxation": {
                "name": "リラックス用",
                "description": "心身のリラックスのためのサウンドスケープ",
                "sounds": [
                    {"id": "waves", "volume": 0.6},
                    {"id": "piano", "volume": 0.4}
                ]
            },
            "meditation": {
                "name": "瞑想用",
                "description": "瞑想に最適なサウンドスケープ",
                "sounds": [
                    {"id": "stream", "volume": 0.5},
                    {"id": "flute", "volume": 0.3}
                ]
            }
        }
    
    def get_all_sounds(self) -> List[Dict[str, Any]]:
        """すべてのサウンドを取得"""
        all_sounds = []
        for category_sounds in self.sounds.values():
            all_sounds.extend(category_sounds.values())
        return all_sounds
    
    def get_sounds_by_category(self, category: str) -> List[Dict[str, Any]]:
        """カテゴリ別にサウンドを取得"""
        return list(self.sounds.get(category, {}).values())
    
    def get_sound_by_id(self, sound_id: str) -> Optional[Dict[str, Any]]:
        """IDでサウンドを取得"""
        for category_sounds in self.sounds.values():
            if sound_id in category_sounds:
                return category_sounds[sound_id]
        return None
    
    def get_presets(self) -> Dict[str, Any]:
        """プリセットサウンドスケープを取得"""
        return self.presets
    
    def get_preset_by_id(self, preset_id: str) -> Optional[Dict[str, Any]]:
        """IDでプリセットを取得"""
        return self.presets.get(preset_id)
    
    def create_custom_soundscape(self, sound_ids: List[str], volumes: List[float] = None) -> Dict[str, Any]:
        """カスタムサウンドスケープを作成"""
        if volumes is None:
            volumes = [0.5] * len(sound_ids)
        
        if len(sound_ids) != len(volumes):
            raise ValueError("サウンドIDとボリュームの数が一致しません")
        
        soundscape = {
            "id": f"custom_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "name": "カスタムサウンドスケープ",
            "description": "ユーザーが作成したカスタムサウンドスケープ",
            "sounds": []
        }
        
        for sound_id, volume in zip(sound_ids, volumes):
            sound = self.get_sound_by_id(sound_id)
            if sound:
                soundscape["sounds"].append({
                    "id": sound_id,
                    "name": sound["name"],
                    "audio_url": sound["audio_url"],
                    "volume": max(0.0, min(1.0, volume))  # 0.0-1.0の範囲に制限
                })
        
        return soundscape
    
    def get_recommended_sounds(self, context: str = None, mood_score: int = None) -> List[Dict[str, Any]]:
        """コンテキストと気分に基づく推奨サウンドを取得"""
        recommendations = []
        
        if context == "sleep" or (mood_score is not None and mood_score <= 2):
            # 睡眠・低い気分：リラックス系
            recommendations.extend([
                self.sounds["nature"]["rain"],
                self.sounds["ambient"]["pink_noise"],
                self.sounds["nature"]["waves"]
            ])
        elif context == "focus" or context == "work":
            # 集中・作業：集中系
            recommendations.extend([
                self.sounds["ambient"]["white_noise"],
                self.sounds["nature"]["forest"],
                self.sounds["instruments"]["piano"]
            ])
        elif context == "meditation":
            # 瞑想：瞑想系
            recommendations.extend([
                self.sounds["nature"]["stream"],
                self.sounds["instruments"]["flute"],
                self.sounds["nature"]["forest"]
            ])
        else:
            # デフォルト：バランスの取れた選択
            recommendations.extend([
                self.sounds["nature"]["waves"],
                self.sounds["instruments"]["piano"],
                self.sounds["ambient"]["pink_noise"]
            ])
        
        return recommendations[:3]  # 最大3つまで
    
    def save_user_favorite(self, user_id: int, soundscape: Dict[str, Any]) -> bool:
        """ユーザーのお気に入りサウンドスケープを保存"""
        try:
            # ジャーナルとして保存
            journal_data = {
                "user_id": user_id,
                "title": f"お気に入りサウンドスケープ - {soundscape['name']}",
                "content": f"サウンドスケープを保存しました。\n\n名前: {soundscape['name']}\n説明: {soundscape.get('description', '')}\n\n含まれるサウンド:\n" + "\n".join([f"• {sound['name']} (ボリューム: {sound['volume']})" for sound in soundscape.get('sounds', [])]),
                "session_type": "soundscape",
                "session_id": soundscape["id"]
            }
            
            SupabaseDB.create_journal(journal_data)
            return True
            
        except Exception as e:
            print(f"サウンドスケープ保存エラー: {e}")
            return False
    
    def get_user_favorites(self, user_id: int) -> List[Dict[str, Any]]:
        """ユーザーのお気に入りサウンドスケープを取得"""
        try:
            journals = SupabaseDB.get_user_journals(user_id)
            soundscape_journals = [
                journal for journal in journals 
                if journal.get('session_type') == 'soundscape'
            ]
            
            return soundscape_journals
            
        except Exception as e:
            print(f"お気に入り取得エラー: {e}")
            return [] 