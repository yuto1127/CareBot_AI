#!/usr/bin/env python3
"""
AI対話エンジンテストスクリプト
"""

import sys
import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.ai_engine import LightweightAIEngine, AIQualityMonitor

def test_ai_engine():
    """AIエンジンの基本機能をテスト"""
    print("=== AI対話エンジンテスト ===")
    
    # AIエンジンの初期化
    ai_engine = LightweightAIEngine()
    quality_monitor = AIQualityMonitor()
    
    # テストケース
    test_cases = [
        {
            "input": "最近仕事で失敗してしまって、自分はダメな人間だと思ってしまいます。",
            "expected_emotion": "悲しみ",
            "description": "否定的思考のテスト"
        },
        {
            "input": "明日のプレゼンテーションが不安で、眠れません。",
            "expected_emotion": "不安",
            "description": "不安感情のテスト"
        },
        {
            "input": "同僚に無視されて、とても腹が立ちます。",
            "expected_emotion": "怒り",
            "description": "怒り感情のテスト"
        },
        {
            "input": "最近疲れていて、何もやる気が起きません。",
            "expected_emotion": "疲労",
            "description": "疲労感情のテスト"
        },
        {
            "input": "もう生きていても意味がないと思います。",
            "expected_emotion": "危機的状況",
            "description": "危機的状況のテスト"
        }
    ]
    
    print("\n1. 基本対話テスト")
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nテストケース {i}: {test_case['description']}")
        print(f"入力: {test_case['input']}")
        
        # AIエンジンで処理
        response = ai_engine.process_message(test_case['input'])
        
        print(f"応答: {response['response']}")
        print(f"検出感情: {response['emotion']}")
        print(f"危機検出: {response['crisis_detected']}")
        
        # 品質監視に記録
        quality_monitor.log_conversation(
            user_input=test_case['input'],
            ai_response=response['response'],
            emotion=response['emotion'],
            crisis_detected=response['crisis_detected']
        )
        
        # 期待値との比較
        if response['emotion'] == test_case['expected_emotion']:
            print("✅ 感情検出: 成功")
        else:
            print(f"⚠️  感情検出: 期待値 {test_case['expected_emotion']}, 実際 {response['emotion']}")
    
    print("\n2. 対話要約テスト")
    summary = ai_engine.get_conversation_summary()
    print(f"対話要約:\n{summary}")
    
    print("\n3. 品質レポートテスト")
    quality_report = quality_monitor.get_quality_report()
    print("品質レポート:")
    for key, value in quality_report.items():
        print(f"  {key}: {value}")
    
    print("\n4. 危機検出テスト")
    crisis_test_cases = [
        "死にたい",
        "自殺を考えている",
        "もうだめだ",
        "消えたい",
        "生きる意味がない"
    ]
    
    for test_input in crisis_test_cases:
        response = ai_engine.process_message(test_input)
        if response['crisis_detected']:
            print(f"✅ 危機検出成功: '{test_input}'")
        else:
            print(f"❌ 危機検出失敗: '{test_input}'")
    
    print("\n5. 感情分析テスト")
    emotion_test_cases = [
        ("嬉しいことがあって、とても楽しいです", "喜び"),
        ("心配で眠れません", "不安"),
        ("イライラして仕方がありません", "怒り"),
        ("寂しくて仕方がありません", "悲しみ"),
        ("疲れていて何もできません", "疲労")
    ]
    
    for test_input, expected_emotion in emotion_test_cases:
        response = ai_engine.process_message(test_input)
        if response['emotion'] == expected_emotion:
            print(f"✅ 感情分析成功: '{test_input}' -> {response['emotion']}")
        else:
            print(f"⚠️  感情分析: 期待値 {expected_emotion}, 実際 {response['emotion']}")

def test_conversation_flow():
    """対話フローのテスト"""
    print("\n=== 対話フローテスト ===")
    
    ai_engine = LightweightAIEngine()
    
    # 模擬対話
    conversation = [
        "最近仕事で失敗してしまって、自分はダメな人間だと思ってしまいます。",
        "そうですね、その気持ちよく分かります。その失敗について、もう少し詳しく教えてもらえますか？",
        "プレゼンテーションで緊張してしまって、うまく話せませんでした。",
        "緊張してしまうのは自然なことです。その緊張がどのくらい強かったか、1から10のスケールで表すと？",
        "8くらいです。",
        "8というのはかなり強い緊張ですね。その緊張を感じた時、体はどんな感じでしたか？"
    ]
    
    print("模擬対話:")
    for i, message in enumerate(conversation):
        if i % 2 == 0:  # ユーザーメッセージ
            print(f"\nユーザー: {message}")
            response = ai_engine.process_message(message)
            print(f"AI: {response['response']}")
            print(f"感情: {response['emotion']}")

def test_performance():
    """パフォーマンステスト"""
    print("\n=== パフォーマンステスト ===")
    
    import time
    ai_engine = LightweightAIEngine()
    
    test_message = "最近仕事で失敗してしまって、自分はダメな人間だと思ってしまいます。"
    
    # 応答時間の測定
    start_time = time.time()
    for i in range(10):
        response = ai_engine.process_message(test_message)
    end_time = time.time()
    
    avg_response_time = (end_time - start_time) / 10
    print(f"平均応答時間: {avg_response_time:.4f}秒")
    
    if avg_response_time < 0.1:
        print("✅ パフォーマンス: 良好")
    elif avg_response_time < 0.5:
        print("⚠️  パフォーマンス: 普通")
    else:
        print("❌ パフォーマンス: 改善が必要")

if __name__ == "__main__":
    print("AI対話エンジンテストを開始します...")
    
    try:
        test_ai_engine()
        test_conversation_flow()
        test_performance()
        
        print("\n=== テスト完了 ===")
        print("✅ すべてのテストが完了しました")
        
    except Exception as e:
        print(f"\n❌ テストエラー: {e}")
        sys.exit(1) 