import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import random
from app.database.supabase_db import SupabaseDB

class CBTAnalyzer:
    """CBT（認知行動療法）対話システム - 完全無料版"""
    
    def __init__(self):
        # OpenAI APIは使用しない（料金発生防止）
        self.client = None
        
        # CBT質問テンプレート
        self.cbt_questions = {
            "evidence": [
                "その考えを裏付ける証拠は何ですか？",
                "その考えが正しいと確信できる理由はありますか？",
                "どんな事実がその考えを支持していますか？"
            ],
            "alternative": [
                "別の考え方はできないでしょうか？",
                "同じ状況を別の角度から見ることはできますか？",
                "他の人ならどう考えるでしょうか？"
            ],
            "worst_case": [
                "最悪のシナリオは何でしょうか？",
                "もしその最悪のことが起きたら、どう対処できますか？",
                "その最悪のシナリオの確率はどのくらいだと思いますか？"
            ],
            "helpful": [
                "その考えはあなたの目標達成に役立っていますか？",
                "その考えはあなたの気分にどのような影響を与えていますか？",
                "より建設的な考え方に変えることはできますか？"
            ],
            "reality": [
                "その考えは現実的ですか？",
                "100%確実にそうだと言えますか？",
                "グレーゾーンはありませんか？"
            ]
        }
        
        # 感情キーワード
        self.emotion_keywords = {
            "anxiety": ["不安", "心配", "怖い", "緊張", "焦り"],
            "anger": ["怒り", "イライラ", "腹が立つ", "憤り"],
            "sadness": ["悲しい", "落ち込み", "辛い", "寂しい"],
            "frustration": ["挫折", "失敗", "ダメ", "できない"],
            "stress": ["ストレス", "疲れ", "限界", "耐えられない"]
        }
    
    def start_cbt_session(self, user_id: int, initial_thought: str = None) -> Dict[str, Any]:
        """CBTセッションを開始"""
        session_id = f"cbt_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # セッション情報を保存
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "start_time": datetime.now().isoformat(),
            "status": "active",
            "conversation": [],
            "initial_thought": initial_thought
        }
        
        # 初回メッセージ
        if initial_thought:
            welcome_message = self._generate_welcome_message_with_thought(initial_thought)
        else:
            welcome_message = self._generate_welcome_message()
        
        session_data["conversation"].append({
            "role": "assistant",
            "content": welcome_message,
            "timestamp": datetime.now().isoformat()
        })
        
        return session_data
    
    def continue_cbt_session(self, session_data: Dict[str, Any], user_message: str) -> Dict[str, Any]:
        """CBTセッションを継続"""
        # ユーザーメッセージを記録
        session_data["conversation"].append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # AI応答を生成
        ai_response = self._generate_cbt_response(session_data["conversation"])
        
        # AI応答を記録
        session_data["conversation"].append({
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now().isoformat()
        })
        
        return session_data
    
    def end_cbt_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """CBTセッションを終了"""
        session_data["status"] = "completed"
        session_data["end_time"] = datetime.now().isoformat()
        
        # セッション要約を生成
        summary = self._generate_session_summary(session_data["conversation"])
        session_data["summary"] = summary
        
        # ジャーナルとして保存
        self._save_as_journal(session_data)
        
        return session_data
    
    def _generate_welcome_message(self) -> str:
        """CBTセッション開始メッセージ"""
        return """こんにちは！CBT（認知行動療法）セッションへようこそ。

私はあなたの思考を整理し、よりバランスの取れた視点を見つけるお手伝いをします。

今日はどんなことでお困りですか？または、最近気になっている考えや感情があれば教えてください。

私は診断や直接的なアドバイスはしません。代わりに、あなた自身がより深く考え、新しい視点を見つけられるよう、質問を投げかけます。

何でもお気軽にお話しください。"""
    
    def _generate_welcome_message_with_thought(self, thought: str) -> str:
        """特定の思考に対するCBTセッション開始メッセージ"""
        return f"""こんにちは！CBT（認知行動療法）セッションへようこそ。

「{thought}」という考えについて、一緒に整理していきましょう。

私は診断や直接的なアドバイスはしません。代わりに、あなた自身がより深く考え、新しい視点を見つけられるよう、質問を投げかけます。

まず、この考えについてもう少し詳しく教えてください。いつ頃からこのように感じていますか？"""
    
    def _generate_cbt_response(self, conversation: List[Dict[str, str]]) -> str:
        """CBT応答を生成（完全無料版）"""
        # OpenAI APIは使用せず、常にフォールバック応答を使用
        return self._generate_enhanced_fallback_response(conversation)
    
    def _generate_enhanced_fallback_response(self, conversation: List[Dict[str, str]]) -> str:
        """高度なフォールバック応答（完全無料版）"""
        user_messages = [msg["content"] for msg in conversation if msg["role"] == "user"]
        if not user_messages:
            return "もう少し詳しく教えてください。"
        
        latest_message = user_messages[-1].lower()
        conversation_length = len(user_messages)
        
        # 感情の種類を判定
        detected_emotion = self._detect_emotion(latest_message)
        
        # 会話の進行度に基づいて質問を選択
        if conversation_length <= 2:
            # 初期段階：感情の詳細化
            return self._generate_exploration_question(detected_emotion, latest_message)
        elif conversation_length <= 4:
            # 中期段階：証拠の検討
            return self._generate_evidence_question(detected_emotion, latest_message)
        elif conversation_length <= 6:
            # 後期段階：代替思考の促進
            return self._generate_alternative_question(detected_emotion, latest_message)
        else:
            # 最終段階：建設的思考の促進
            return self._generate_constructive_question(detected_emotion, latest_message)
    
    def _detect_emotion(self, message: str) -> str:
        """メッセージから感情を検出"""
        for emotion, keywords in self.emotion_keywords.items():
            if any(keyword in message for keyword in keywords):
                return emotion
        return "general"
    
    def _generate_exploration_question(self, emotion: str, message: str) -> str:
        """感情の詳細化質問"""
        if emotion == "anxiety":
            return random.choice([
                "その不安について、もう少し詳しく教えてください。いつ頃からそのように感じていますか？",
                "不安を感じる具体的な状況はありますか？",
                "その不安の強さはどのくらいですか？（1-10のスケールで）"
            ])
        elif emotion == "anger":
            return random.choice([
                "その怒りの感情について、どんな状況で感じましたか？",
                "怒りを感じる前には、どんなことがありましたか？",
                "その怒りは、あなたの行動にどのような影響を与えていますか？"
            ])
        elif emotion == "sadness":
            return random.choice([
                "その気持ちについて、もう少し詳しく教えてください。",
                "悲しい気持ちが続いている期間はどのくらいですか？",
                "その気持ちが最も強く感じられるのは、どんな時ですか？"
            ])
        elif emotion == "frustration":
            return random.choice([
                "その挫折感について、具体的にどんな証拠がありますか？",
                "失敗と感じる基準は何ですか？",
                "その考えが正しいと確信できる理由はありますか？"
            ])
        else:
            return random.choice([
                "その考えについて、もう少し詳しく教えてください。",
                "いつ、どんな状況でそのように感じましたか？",
                "その気持ちが生まれるきっかけは何でしたか？"
            ])
    
    def _generate_evidence_question(self, emotion: str, message: str) -> str:
        """証拠の検討質問"""
        return random.choice(self.cbt_questions["evidence"]) + "\n\nまた、" + random.choice([
            "その考えは現実的ですか？",
            "100%確実にそうだと言えますか？",
            "グレーゾーンはありませんか？"
        ])
    
    def _generate_alternative_question(self, emotion: str, message: str) -> str:
        """代替思考の促進質問"""
        return random.choice(self.cbt_questions["alternative"]) + "\n\nさらに、" + random.choice([
            "同じ状況を別の角度から見ることはできますか？",
            "他の人ならどう考えるでしょうか？",
            "過去に似たような状況で、うまく対処できた経験はありますか？"
        ])
    
    def _generate_constructive_question(self, emotion: str, message: str) -> str:
        """建設的思考の促進質問"""
        return random.choice(self.cbt_questions["helpful"]) + "\n\nそして、" + random.choice([
            "より建設的な考え方に変えることはできますか？",
            "この状況から学べることはありますか？",
            "次回同じような状況になった時、どう対処したいですか？"
        ])
    
    def _generate_fallback_response(self, conversation: List[Dict[str, str]]) -> str:
        """従来のフォールバック応答（後方互換性のため残存）"""
        return self._generate_enhanced_fallback_response(conversation)
    
    def _generate_session_summary(self, conversation: List[Dict[str, str]]) -> str:
        """セッション要約を生成"""
        user_messages = [msg["content"] for msg in conversation if msg["role"] == "user"]
        ai_messages = [msg["content"] for msg in conversation if msg["role"] == "assistant"]
        
        if not user_messages:
            return "セッションが開始されましたが、詳細な対話は記録されていません。"
        
        # 簡単な要約生成
        summary = f"CBTセッションが完了しました。\n\n"
        summary += f"対話回数: {len(user_messages)}回\n"
        summary += f"主な話題: {user_messages[0][:50]}...\n\n"
        summary += "このセッションの内容は、あなたのジャーナルに自動保存されました。"
        
        return summary
    
    def _save_as_journal(self, session_data: Dict[str, Any]) -> bool:
        """CBTセッションをジャーナルとして保存"""
        try:
            # 会話内容をテキストに変換
            conversation_text = ""
            for msg in session_data["conversation"]:
                role = "あなた" if msg["role"] == "user" else "AI"
                conversation_text += f"{role}: {msg['content']}\n\n"
            
            # ジャーナルとして保存
            journal_data = {
                "user_id": session_data["user_id"],
                "title": f"CBTセッション - {session_data['session_id']}",
                "content": conversation_text,
                "session_type": "cbt",
                "session_id": session_data["session_id"],
                "summary": session_data.get("summary", "")
            }
            
            SupabaseDB.create_journal(journal_data)
            return True
            
        except Exception as e:
            print(f"ジャーナル保存エラー: {e}")
            return False
    
    def detect_crisis(self, message: str) -> bool:
        """危機的状況を検知"""
        crisis_keywords = [
            "死にたい", "自殺", "消えたい", "生きる意味がない",
            "もう限界", "耐えられない", "終わりにしたい"
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in crisis_keywords)
    
    def get_crisis_response(self) -> str:
        """危機的状況に対する応答"""
        return """お話を聞かせていただき、ありがとうございます。

あなたの気持ちはとても大切です。今、とても辛い状況にいらっしゃるようですね。

専門家に相談することをお勧めします。以下の機関に24時間いつでも相談できます：

• いのちの電話: 0120-783-556
• よりそいホットライン: 0120-279-338
• チャイルドライン: 0120-99-7777

また、お近くの精神保健福祉センターや心療内科にも相談できます。

あなたは一人ではありません。必ず助けがあります。""" 