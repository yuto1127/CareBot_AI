# AI対話エンジン実装手順

## 1. 基盤モデルの選定とセットアップ

### 1.1 モデル選定
- **モデル**: `stabilityai/japanese-stablelm-instruct-gamma-7B`
- **理由**: 
  - Apache 2.0ライセンス（商用利用可能）
  - 7Bパラメータ（軽量で個人開発に適している）
  - 日本語特化
  - GGUF形式で量子化可能

### 1.2 Ollamaセットアップ
```bash
# Ollamaのインストール
curl -fsSL https://ollama.ai/install.sh | sh

# モデルのダウンロード
ollama pull japanese-stablelm-instruct-gamma-7b

# 量子化版の作成（オプション）
ollama create cbt-coach -f Modelfile
```

### 1.3 Modelfile作成
```dockerfile
FROM japanese-stablelm-instruct-gamma-7b

# システムプロンプトの設定
SYSTEM """
あなたは認知行動療法（CBT）の原則に基づき、ユーザーの自己理解を助ける、共感的で思慮深いAIコーチです。

【役割】
- ユーザーの思考プロセスを整理する手助け
- ソクラテス式質問法による内省促進
- 決して診断や断定的なアドバイスは行わない
- ユーザーの感情を否定しない

【行動規範】
1. 共感的で受容的な態度を保つ
2. ユーザー自身の気づきを促す質問をする
3. 危機的状況の場合は専門機関への相談を促す
4. 対話内容は自動的にジャーナルとして記録される

【制約】
- 医療診断は行わない
- 薬の処方や治療法の提案は行わない
- ユーザーの安全が脅かされる場合は対話を中断
"""
```

## 2. プロンプトエンジニアリング

### 2.1 システムプロンプト設計
```python
# backend/app/utils/ai_prompts.py
CBT_SYSTEM_PROMPT = """
あなたは認知行動療法（CBT）の原則に基づくAIコーチです。

【基本方針】
- ソクラテス式質問法でユーザーの内省を促す
- 思考記録（ソートレコード）のプロセスをガイド
- 共感的で受容的な態度を保つ

【質問例】
- 「その考えを裏付ける証拠はありますか？」
- 「別の考え方はできないでしょうか？」
- 「もし友人が同じ状況だったら、何と言いますか？」

【安全性】
- 危機的状況の場合は専門機関への相談を促す
- 自傷行為の示唆がある場合は対話を中断
"""

CRISIS_DETECTION_PROMPT = """
以下のキーワードが検出された場合、即座に対話を中断し、
専門機関への相談を促すメッセージのみを表示してください：

- 自殺、死にたい、消えたい
- 自傷、リストカット
- 絶望的、もうだめだ
- 誰もいない、孤独

【対応メッセージ】
「お話を聞かせていただき、ありがとうございます。
今の状況について、専門家に相談することをお勧めします。
24時間対応の相談窓口があります：
- いのちの電話：0570-783-556
- よりそいホットライン：0120-279-338
すぐに相談できる専門家がいます。」
"""
```

### 2.2 対話ルーター実装
```python
# backend/app/utils/ai_router.py
class AIRouter:
    def __init__(self):
        self.local_model = "cbt-coach"  # Ollamaモデル名
        self.external_api = "openai"     # 外部API
    
    async def route_conversation(self, user_input: str, context: dict):
        """対話の複雑さに応じてモデルを振り分け"""
        
        # 危機的状況の検出
        if self._detect_crisis(user_input):
            return self._handle_crisis(user_input)
        
        # 複雑度の判定
        complexity = self._assess_complexity(user_input, context)
        
        if complexity > 0.8:  # 高複雑度
            return await self._call_external_api(user_input, context)
        else:  # 通常の対話
            return await self._call_local_model(user_input, context)
    
    def _detect_crisis(self, text: str) -> bool:
        """危機的状況のキーワード検出"""
        crisis_keywords = [
            "自殺", "死にたい", "消えたい", "自傷", "リストカット",
            "絶望的", "もうだめだ", "誰もいない", "孤独"
        ]
        return any(keyword in text for keyword in crisis_keywords)
    
    def _assess_complexity(self, text: str, context: dict) -> float:
        """対話の複雑度を0-1で評価"""
        # 実装例：文章の長さ、感情表現の複雑さ、文脈の深さを考慮
        pass
```

## 3. ファインチューニング準備

### 3.1 合成データ生成
```python
# backend/scripts/generate_training_data.py
import openai
from typing import List, Dict

class CBTDataGenerator:
    def __init__(self):
        self.openai_client = openai.OpenAI()
    
    def generate_cbt_conversations(self) -> List[Dict]:
        """CBT対話の合成データを生成"""
        
        scenarios = [
            "仕事での失敗に対する否定的思考",
            "人間関係での不安",
            "将来への不安",
            "完璧主義的な思考",
            "他者との比較による劣等感"
        ]
        
        conversations = []
        
        for scenario in scenarios:
            # GPT-4oを使用してCBT対話を生成
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": CBT_SYSTEM_PROMPT},
                    {"role": "user", "content": f"以下のシナリオでCBT対話を生成してください：{scenario}"}
                ]
            )
            
            conversations.append({
                "scenario": scenario,
                "conversation": response.choices[0].message.content
            })
        
        return conversations
```

### 3.2 ファインチューニング実行
```bash
# ファインチューニング用のスクリプト
python backend/scripts/fine_tune_cbt.py
```

## 4. 統合実装

### 4.1 FastAPIエンドポイント
```python
# backend/app/api/endpoints/cbt.py
from fastapi import APIRouter, Depends, HTTPException
from app.utils.ai_router import AIRouter
from app.schemas.cbt import CBTRequest, CBTResponse

router = APIRouter(tags=["cbt"])
ai_router = AIRouter()

@router.post("/conversation", response_model=CBTResponse)
async def cbt_conversation(
    request: CBTRequest,
    current_user: dict = Depends(get_current_user)
):
    """CBT対話セッション"""
    
    try:
        # 対話の実行
        response = await ai_router.route_conversation(
            user_input=request.message,
            context=request.context
        )
        
        # ジャーナルとして記録
        await record_conversation(
            user_id=current_user['id'],
            message=request.message,
            response=response,
            context=request.context
        )
        
        return CBTResponse(
            message=response,
            session_id=request.session_id
        )
        
    except Exception as e:
        logger.error("CBT対話エラー", e, {"user_id": current_user['id']})
        raise HTTPException(status_code=500, detail="対話の処理中にエラーが発生しました")
```

### 4.2 フロントエンド統合
```typescript
// frontend/src/lib/cbt.ts
export class CBTSession {
    private sessionId: string;
    private context: any = {};
    
    constructor() {
        this.sessionId = crypto.randomUUID();
    }
    
    async sendMessage(message: string): Promise<string> {
        const response = await api.post('/api/cbt/conversation', {
            message,
            session_id: this.sessionId,
            context: this.context
        });
        
        // コンテキストを更新
        this.context = response.data.context;
        
        return response.data.message;
    }
}
```

## 5. 安全性と品質保証

### 5.1 危機対応プロトコル
```python
# backend/app/utils/crisis_handler.py
class CrisisHandler:
    def __init__(self):
        self.crisis_keywords = [
            "自殺", "死にたい", "消えたい", "自傷", "リストカット",
            "絶望的", "もうだめだ", "誰もいない", "孤独"
        ]
    
    def detect_crisis(self, text: str) -> bool:
        """危機的状況の検出"""
        return any(keyword in text for keyword in self.crisis_keywords)
    
    def get_crisis_response(self) -> str:
        """危機対応メッセージ"""
        return """
        お話を聞かせていただき、ありがとうございます。
        今の状況について、専門家に相談することをお勧めします。
        
        24時間対応の相談窓口があります：
        - いのちの電話：0570-783-556
        - よりそいホットライン：0120-279-338
        
        すぐに相談できる専門家がいます。
        """
```

### 5.2 品質監視
```python
# backend/app/utils/quality_monitor.py
class QualityMonitor:
    def __init__(self):
        self.metrics = {}
    
    def log_conversation(self, user_input: str, ai_response: str, quality_score: float):
        """対話品質の記録"""
        # 実装：対話の品質を評価し、改善に活用
        pass
    
    def detect_inappropriate_response(self, response: str) -> bool:
        """不適切な応答の検出"""
        # 実装：不適切な応答を検出
        pass
```

## 6. デプロイと運用

### 6.1 本番環境設定
```yaml
# docker-compose.yml
version: '3.8'
services:
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
  
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_URL=http://ollama:11434
    depends_on:
      - ollama

volumes:
  ollama_data:
```

### 6.2 監視とログ
```python
# backend/app/utils/monitoring.py
class AIUsageMonitor:
    def __init__(self):
        self.usage_stats = {}
    
    def log_ai_request(self, model: str, response_time: float, quality_score: float):
        """AI使用状況の記録"""
        # 実装：使用統計の記録
        pass
    
    def get_usage_report(self) -> dict:
        """使用状況レポート"""
        # 実装：使用統計の集計
        pass
```

## 7. 次のステップ

1. **Ollamaのセットアップとモデル導入**
2. **基本的なプロンプト設計とテスト**
3. **危機対応プロトコルの実装**
4. **フロントエンドとの統合**
5. **品質監視システムの構築**
6. **ファインチューニングの実行**
7. **本番環境へのデプロイ** 