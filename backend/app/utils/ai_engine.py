"""
コスト最適化AI対話エンジン
軽量なプロンプトベースのCBT特化AIエンジン
"""

import re
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json

class LightweightAIEngine:
    """軽量なCBT特化AIエンジン"""
    
    def __init__(self):
        self.crisis_keywords = [
            "自殺", "死にたい", "消えたい", "自傷", "リストカット",
            "絶望的", "もうだめだ", "誰もいない", "孤独", "生きる意味がない",
            "死ね", "消えたい", "終わりたい", "生きていても意味がない"
        ]
        
        self.cbt_questions = [
            "その考えを裏付ける証拠はありますか？",
            "別の考え方はできないでしょうか？",
            "もし友人が同じ状況だったら、何と言いますか？",
            "その考えは100%確実ですか？",
            "最悪の事態が起きたとして、それでも対処できますか？",
            "その状況の良い面はありますか？",
            "過去に似たような経験はありますか？",
            "その考えが事実と感情のどちらに基づいていますか？"
        ]
        
        self.emotion_keywords = {
            "不安": [
                "心配", "緊張", "恐れ", "怖い", "ドキドキ", "不安", "プレゼンテーション",
                "失敗", "うまく", "緊張", "心配", "怖い", "恐れる", "不安定"
            ],
            "怒り": [
                "イライラ", "腹が立つ", "憤り", "激怒", "怒り", "腹立ち", "イラつく",
                "無視", "腹が立つ", "怒る", "憤る", "激怒", "怒り", "腹立ち"
            ],
            "悲しみ": [
                "落ち込む", "寂しい", "切ない", "涙", "悲しい", "落ち込み", "寂しさ",
                "ダメ", "失敗", "落ち込む", "悲しい", "切ない", "寂しい", "涙"
            ],
            "喜び": [
                "嬉しい", "楽しい", "幸せ", "満足", "喜び", "嬉しさ", "楽しさ",
                "成功", "嬉しい", "楽しい", "幸せ", "満足", "喜び", "嬉しさ"
            ],
            "疲労": [
                "疲れた", "だるい", "やる気がない", "消耗", "疲労", "疲れ", "だるさ",
                "やる気", "疲れた", "だるい", "やる気がない", "消耗", "疲労"
            ]
        }
        
        self.context = {}
    
    def process_message(self, user_input: str, user_id: int = None) -> Dict[str, any]:
        """ユーザーメッセージを処理してAI応答を生成"""
        
        # 危機的状況の検出
        if self._detect_crisis(user_input):
            return self._handle_crisis()
        
        # 感情の分析
        emotion = self._analyze_emotion(user_input)
        
        # CBT質問の生成
        response = self._generate_cbt_response(user_input, emotion)
        
        # コンテキストの更新
        self._update_context(user_input, response, emotion)
        
        return {
            "response": response,
            "emotion": emotion,
            "crisis_detected": False,
            "timestamp": datetime.now().isoformat(),
            "context": self.context
        }
    
    def _detect_crisis(self, text: str) -> bool:
        """危機的状況のキーワード検出"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.crisis_keywords)
    
    def _handle_crisis(self) -> Dict[str, any]:
        """危機的状況への対応"""
        crisis_response = """
お話を聞かせていただき、ありがとうございます。
今の状況について、専門家に相談することをお勧めします。

24時間対応の相談窓口があります：
- いのちの電話：0570-783-556
- よりそいホットライン：0120-279-338

すぐに相談できる専門家がいます。
"""
        
        return {
            "response": crisis_response,
            "emotion": "危機的状況",
            "crisis_detected": True,
            "timestamp": datetime.now().isoformat(),
            "context": self.context
        }
    
    def _analyze_emotion(self, text: str) -> str:
        """感情の分析（改善版）"""
        text_lower = text.lower()
        
        # 各感情のキーワードマッチ数をカウント
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            if score > 0:
                emotion_scores[emotion] = score
        
        # 最もスコアの高い感情を返す
        if emotion_scores:
            dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
            return dominant_emotion
        
        # 感情が特定できない場合のデフォルト
        return "不明"
    
    def _generate_cbt_response(self, user_input: str, emotion: str) -> str:
        """CBT応答の生成"""
        
        # 感情に応じた応答の選択
        if emotion == "不安":
            return self._generate_anxiety_response(user_input)
        elif emotion == "怒り":
            return self._generate_anger_response(user_input)
        elif emotion == "悲しみ":
            return self._generate_sadness_response(user_input)
        elif emotion == "疲労":
            return self._generate_fatigue_response(user_input)
        elif emotion == "喜び":
            return self._generate_joy_response(user_input)
        else:
            return self._generate_general_response(user_input)
    
    def _generate_anxiety_response(self, user_input: str) -> str:
        """不安に対する応答"""
        responses = [
            "その不安な気持ち、よく分かります。まず、その不安がどのくらい強いか教えてもらえますか？1から10のスケールで表すと？",
            "不安を感じるのは自然なことです。その不安の原因について、もう少し詳しく話してもらえますか？",
            "不安な時は、呼吸を整えることが役立ちます。一緒に深呼吸してみませんか？",
            "その不安について、具体的に何が心配なのか教えてもらえますか？"
        ]
        return random.choice(responses)
    
    def _generate_anger_response(self, user_input: str) -> str:
        """怒りに対する応答"""
        responses = [
            "その怒りの気持ち、理解できます。何が一番腹が立ちますか？",
            "怒りを感じるのは当然です。その怒りがどこから来ているのか、考えてみませんか？",
            "怒りを感じている時は、少し時間を置いてから考えるのも良いかもしれません。",
            "その怒りについて、もう少し詳しく教えてもらえますか？"
        ]
        return random.choice(responses)
    
    def _generate_sadness_response(self, user_input: str) -> str:
        """悲しみに対する応答"""
        responses = [
            "その悲しい気持ち、よく分かります。無理に明るくする必要はありません。",
            "悲しい時は、自分のペースでゆっくりと過ごすことが大切です。",
            "その悲しみについて、もう少し詳しく話してもらえますか？",
            "悲しい気持ちを感じるのは自然なことです。その気持ちを否定する必要はありません。"
        ]
        return random.choice(responses)
    
    def _generate_fatigue_response(self, user_input: str) -> str:
        """疲労に対する応答"""
        responses = [
            "お疲れのようですね。無理をしすぎていませんか？",
            "疲れている時は、休息を取ることが大切です。何かリラックスできることはありますか？",
            "その疲れの原因について、考えてみませんか？",
            "疲れている時は、自分のペースで過ごすことが大切です。"
        ]
        return random.choice(responses)
    
    def _generate_joy_response(self, user_input: str) -> str:
        """喜びに対する応答"""
        responses = [
            "その嬉しい気持ち、素晴らしいですね。何が一番嬉しかったですか？",
            "喜びを感じるのは素晴らしいことです。その喜びについて、もう少し詳しく教えてもらえますか？",
            "その幸せな気持ちを大切にしてください。何がその喜びをもたらしたのでしょうか？",
            "嬉しいことがあるのは素晴らしいですね。その気持ちを味わってください。"
        ]
        return random.choice(responses)
    
    def _generate_general_response(self, user_input: str) -> str:
        """一般的な応答"""
        # CBT質問からランダムに選択
        question = random.choice(self.cbt_questions)
        
        # 共感的な前置きを追加
        empathetic_prefixes = [
            "その気持ち、よく分かります。",
            "お話を聞かせていただき、ありがとうございます。",
            "その状況について、もう少し詳しく教えてもらえますか？"
        ]
        
        prefix = random.choice(empathetic_prefixes)
        return f"{prefix} {question}"
    
    def _update_context(self, user_input: str, response: str, emotion: str):
        """対話コンテキストの更新"""
        if "conversation_history" not in self.context:
            self.context["conversation_history"] = []
        
        self.context["conversation_history"].append({
            "user_input": user_input,
            "ai_response": response,
            "emotion": emotion,
            "timestamp": datetime.now().isoformat()
        })
        
        # 履歴を最新の10件に制限
        if len(self.context["conversation_history"]) > 10:
            self.context["conversation_history"] = self.context["conversation_history"][-10:]
    
    def get_conversation_summary(self) -> str:
        """対話の要約を生成"""
        if "conversation_history" not in self.context:
            return "まだ対話が始まっていません。"
        
        history = self.context["conversation_history"]
        if not history:
            return "まだ対話が始まっていません。"
        
        # 感情の傾向を分析
        emotions = [entry["emotion"] for entry in history]
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # 最も多い感情を特定
        dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
        
        summary = f"""
対話の要約：
- 対話回数: {len(history)}回
- 主要な感情: {dominant_emotion}
- 最後の対話: {history[-1]['timestamp']}
"""
        
        return summary

class AIQualityMonitor:
    """AI応答の品質監視"""
    
    def __init__(self):
        self.quality_metrics = {
            "total_conversations": 0,
            "crisis_detections": 0,
            "average_response_length": 0,
            "emotion_distribution": {}
        }
    
    def log_conversation(self, user_input: str, ai_response: str, emotion: str, crisis_detected: bool):
        """対話の品質を記録"""
        self.quality_metrics["total_conversations"] += 1
        
        if crisis_detected:
            self.quality_metrics["crisis_detections"] += 1
        
        # 感情分布の更新
        if emotion not in self.quality_metrics["emotion_distribution"]:
            self.quality_metrics["emotion_distribution"][emotion] = 0
        self.quality_metrics["emotion_distribution"][emotion] += 1
        
        # 平均応答長の更新
        current_avg = self.quality_metrics["average_response_length"]
        new_length = len(ai_response)
        total_conversations = self.quality_metrics["total_conversations"]
        
        self.quality_metrics["average_response_length"] = (
            (current_avg * (total_conversations - 1) + new_length) / total_conversations
        )
    
    def get_quality_report(self) -> Dict[str, any]:
        """品質レポートを生成"""
        return {
            "total_conversations": self.quality_metrics["total_conversations"],
            "crisis_detection_rate": (
                self.quality_metrics["crisis_detections"] / 
                max(self.quality_metrics["total_conversations"], 1)
            ),
            "average_response_length": self.quality_metrics["average_response_length"],
            "emotion_distribution": self.quality_metrics["emotion_distribution"]
        } 