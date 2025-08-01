#!/usr/bin/env python3
"""
CBT APIエンドポイントテストスクリプト
"""

import requests
import json
import time
from typing import Dict, Any

# API設定
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def test_cbt_session():
    """CBTセッション開始のテスト"""
    print("=== CBTセッション開始テスト ===")
    
    # まずログインしてトークンを取得
    login_data = {
        "email": "test@example.com",
        "password": "Test1234"
    }
    
    try:
        # ログイン
        login_response = requests.post(f"{API_BASE}/auth/login", json=login_data)
        if login_response.status_code != 200:
            print(f"❌ ログイン失敗: {login_response.status_code}")
            print(f"レスポンス: {login_response.text}")
            return None
        
        login_result = login_response.json()
        token = login_result.get("access_token")
        
        if not token:
            print("❌ トークンが取得できませんでした")
            return None
        
        print("✅ ログイン成功")
        
        # ヘッダー設定
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # CBTセッション開始
        session_data = {
            "initial_message": "最近仕事で失敗してしまって、自分はダメな人間だと思ってしまいます。"
        }
        
        session_response = requests.post(
            f"{API_BASE}/cbt/session",
            json=session_data,
            headers=headers
        )
        
        if session_response.status_code == 200:
            session_result = session_response.json()
            print("✅ CBTセッション開始成功")
            print(f"セッションID: {session_result.get('session_id')}")
            print(f"歓迎メッセージ: {session_result.get('welcome_message')[:100]}...")
            return token, session_result.get('session_id')
        else:
            print(f"❌ CBTセッション開始失敗: {session_response.status_code}")
            print(f"レスポンス: {session_response.text}")
            return None
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        return None

def test_cbt_conversation(token: str, session_id: str):
    """CBT対話のテスト"""
    print("\n=== CBT対話テスト ===")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # テストメッセージ
    test_messages = [
        "最近仕事で失敗してしまって、自分はダメな人間だと思ってしまいます。",
        "明日のプレゼンテーションが不安で、眠れません。",
        "同僚に無視されて、とても腹が立ちます。",
        "最近疲れていて、何もやる気が起きません。",
        "もう生きていても意味がないと思います。"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n--- 対話 {i} ---")
        print(f"ユーザー: {message}")
        
        conversation_data = {
            "message": message,
            "session_id": session_id
        }
        
        try:
            response = requests.post(
                f"{API_BASE}/cbt/conversation",
                json=conversation_data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"AI: {result.get('message')}")
                print(f"感情: {result.get('emotion')}")
                print(f"危機検出: {result.get('crisis_detected')}")
                
                # 危機的状況の場合は特別な処理
                if result.get('crisis_detected'):
                    print("⚠️  危機的状況が検出されました")
                
            else:
                print(f"❌ 対話失敗: {response.status_code}")
                print(f"レスポンス: {response.text}")
                
        except Exception as e:
            print(f"❌ エラー: {e}")
        
        # 対話間に少し待機
        time.sleep(1)

def test_conversation_summary(token: str):
    """対話要約のテスト"""
    print("\n=== 対話要約テスト ===")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{API_BASE}/cbt/conversation/summary",
            headers=headers
        )
        
        if response.status_code == 200:
            summary = response.text
            print("✅ 対話要約取得成功")
            print(f"要約: {summary}")
        else:
            print(f"❌ 対話要約取得失敗: {response.status_code}")
            print(f"レスポンス: {response.text}")
            
    except Exception as e:
        print(f"❌ エラー: {e}")

def test_quality_report(token: str):
    """品質レポートのテスト"""
    print("\n=== 品質レポートテスト ===")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{API_BASE}/cbt/quality/report",
            headers=headers
        )
        
        if response.status_code == 200:
            report = response.json()
            print("✅ 品質レポート取得成功")
            print("品質レポート:")
            for key, value in report.items():
                print(f"  {key}: {value}")
        elif response.status_code == 403:
            print("⚠️  管理者権限が必要です（これは正常な動作です）")
        else:
            print(f"❌ 品質レポート取得失敗: {response.status_code}")
            print(f"レスポンス: {response.text}")
            
    except Exception as e:
        print(f"❌ エラー: {e}")

def main():
    """メイン関数"""
    print("CBT APIエンドポイントテストを開始します...")
    
    # サーバーが起動しているか確認
    try:
        health_check = requests.get(f"{BASE_URL}/docs")
        if health_check.status_code != 200:
            print("❌ サーバーが起動していません")
            print("python main.py でサーバーを起動してください")
            return
        print("✅ サーバーが起動しています")
    except Exception as e:
        print("❌ サーバーに接続できません")
        print("python main.py でサーバーを起動してください")
        return
    
    # CBTセッション開始
    result = test_cbt_session()
    if result is None:
        print("❌ CBTセッション開始に失敗しました")
        return
    
    token, session_id = result
    
    # CBT対話テスト
    test_cbt_conversation(token, session_id)
    
    # 対話要約テスト
    test_conversation_summary(token)
    
    # 品質レポートテスト
    test_quality_report(token)
    
    print("\n=== テスト完了 ===")
    print("✅ すべてのテストが完了しました")

if __name__ == "__main__":
    main() 