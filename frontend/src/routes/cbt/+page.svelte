<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { fetchAPI } from '$lib/api';
  
  let sessionId: string | null = null;
  let messages: Array<{role: 'user' | 'assistant', content: string, timestamp: string}> = [];
  let currentMessage = '';
  let loading = false;
  let error = '';
  let isLoggedIn = false;
  let initialThought = '';
  let showInitialThoughtInput = true;
  
  onMount(async () => {
    // ログイン状態チェック
    const user = localStorage.getItem('user');
    if (!user) {
      isLoggedIn = false;
      return;
    }
    isLoggedIn = true;
  });
  
  async function startSession() {
    if (!initialThought.trim()) {
      error = '最初の考えを入力してください';
      return;
    }
    
    loading = true;
    error = '';
    
    try {
      const response = await fetchAPI('/cbt/session/start', {
        method: 'POST',
        body: JSON.stringify({ initial_thought: initialThought })
      });
      
      sessionId = response.session_id;
      messages = [{
        role: 'assistant',
        content: response.message,
        timestamp: new Date().toISOString()
      }];
      showInitialThoughtInput = false;
      
    } catch (err: any) {
      if (err.status === 429) {
        error = 'CBTセッションの使用回数上限に達しました。プレミアムプランへのアップグレードをご検討ください。';
      } else {
        error = 'セッション開始に失敗しました: ' + (err.message || '不明なエラー');
      }
    } finally {
      loading = false;
    }
  }
  
  async function sendMessage() {
    if (!currentMessage.trim() || !sessionId) return;
    
    const userMessage = currentMessage;
    currentMessage = '';
    loading = true;
    
    // ユーザーメッセージを追加
    messages = [...messages, {
      role: 'user',
      content: userMessage,
      timestamp: new Date().toISOString()
    }];
    
    try {
      const response = await fetchAPI(`/cbt/session/${sessionId}/continue`, {
        method: 'POST',
        body: JSON.stringify({ message: userMessage })
      });
      
      // AI応答を追加
      messages = [...messages, {
        role: 'assistant',
        content: response.message,
        timestamp: new Date().toISOString()
      }];
      
      // 危機的状況が検知された場合
      if (response.crisis_detected) {
        // 特別な処理（例：専門機関へのリンク表示など）
        console.log('危機的状況が検知されました');
      }
      
    } catch (err: any) {
      error = 'メッセージ送信に失敗しました: ' + (err.message || '不明なエラー');
      // エラーメッセージを追加
      messages = [...messages, {
        role: 'assistant',
        content: '申し訳ございません。エラーが発生しました。もう一度お試しください。',
        timestamp: new Date().toISOString()
      }];
    } finally {
      loading = false;
    }
  }
  
  async function endSession() {
    if (!sessionId) return;
    
    loading = true;
    
    try {
      const response = await fetchAPI(`/cbt/session/${sessionId}/end`, {
        method: 'POST'
      });
      
      // セッション終了メッセージを追加
      messages = [...messages, {
        role: 'assistant',
        content: response.message,
        timestamp: new Date().toISOString()
      }];
      
      // 要約を表示
      if (response.summary) {
        messages = [...messages, {
          role: 'assistant',
          content: `\n--- セッション要約 ---\n${response.summary}`,
          timestamp: new Date().toISOString()
        }];
      }
      
      sessionId = null;
      
    } catch (err: any) {
      error = 'セッション終了に失敗しました: ' + (err.message || '不明なエラー');
    } finally {
      loading = false;
    }
  }
  
  function handleKeyPress(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      if (showInitialThoughtInput) {
        startSession();
      } else {
        sendMessage();
      }
    }
  }
</script>

<svelte:head>
  <title>CBTセッション - CareBot AI</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
  <div class="max-w-4xl mx-auto">
    <!-- ヘッダー -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">CBT（認知行動療法）セッション</h1>
          <p class="text-gray-600 mt-2">
            あなたの思考を整理し、よりバランスの取れた視点を見つけるお手伝いをします
          </p>
        </div>
        <div class="flex gap-2">
          {#if !isLoggedIn}
            <a href="/login" class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors">
              ログイン
            </a>
            <a href="/register" class="bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600 transition-colors">
              新規登録
            </a>
          {:else}
            <a href="/dashboard" class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors">
              ダッシュボード
            </a>
            <a href="/profile" class="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600 transition-colors">
              プロフィール
            </a>
          {/if}
        </div>
      </div>
    </div>

    {#if !isLoggedIn}
      <!-- ログインが必要 -->
      <div class="bg-white rounded-lg shadow-md p-8 text-center">
        <div class="text-6xl mb-4">🔒</div>
        <h2 class="text-xl font-semibold text-gray-800 mb-4">ログインが必要です</h2>
        <p class="text-gray-600 mb-6">
          CBTセッションを利用するには、アカウントにログインしてください。
        </p>
        <a href="/login" class="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors">
          ログインする
        </a>
      </div>
    {:else}
      <!-- CBTセッション -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <!-- チャットエリア -->
        <div class="h-96 overflow-y-auto p-6 space-y-4" id="chat-area">
          {#if showInitialThoughtInput}
            <!-- 初期思考入力 -->
            <div class="text-center py-8">
              <div class="text-4xl mb-4">🧠</div>
              <h3 class="text-lg font-semibold text-gray-800 mb-4">
                今日はどんなことでお困りですか？
              </h3>
              <p class="text-gray-600 mb-6">
                最近気になっている考えや感情があれば教えてください。
              </p>
              <div class="max-w-md mx-auto">
                <textarea
                  bind:value={initialThought}
                  on:keypress={handleKeyPress}
                  placeholder="例：仕事で失敗してしまい、自分はダメだと思ってしまう..."
                  class="w-full p-3 border border-gray-300 rounded-lg resize-none h-24 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  disabled={loading}
                ></textarea>
                <button
                  on:click={startSession}
                  disabled={loading || !initialThought.trim()}
                  class="mt-3 w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? 'セッション開始中...' : 'セッションを開始'}
                </button>
              </div>
            </div>
          {:else}
            <!-- メッセージ表示 -->
            {#each messages as message}
              <div class="flex {message.role === 'user' ? 'justify-end' : 'justify-start'}">
                <div class="max-w-xs lg:max-w-md">
                  <div class="p-3 rounded-lg {message.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-800'}">
                    <div class="whitespace-pre-wrap">{message.content}</div>
                    <div class="text-xs opacity-70 mt-1">
                      {new Date(message.timestamp).toLocaleTimeString()}
                    </div>
                  </div>
                </div>
              </div>
            {/each}
            
            {#if loading}
              <div class="flex justify-start">
                <div class="max-w-xs lg:max-w-md">
                  <div class="bg-gray-100 text-gray-800 p-3 rounded-lg">
                    <div class="flex items-center space-x-2">
                      <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-600"></div>
                      <span>考え中...</span>
                    </div>
                  </div>
                </div>
              </div>
            {/if}
          {/if}
        </div>

        <!-- エラーメッセージ -->
        {#if error}
          <div class="bg-red-50 border-l-4 border-red-400 p-4 mx-6 mb-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        {/if}

        <!-- 入力エリア -->
        {#if !showInitialThoughtInput}
          <div class="border-t border-gray-200 p-4">
            <div class="flex space-x-2">
              <textarea
                bind:value={currentMessage}
                on:keypress={handleKeyPress}
                placeholder="メッセージを入力してください..."
                class="flex-1 p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows="2"
                disabled={loading}
              ></textarea>
              <div class="flex flex-col space-y-2">
                <button
                  on:click={sendMessage}
                  disabled={loading || !currentMessage.trim()}
                  class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                >
                  送信
                </button>
                <button
                  on:click={endSession}
                  disabled={loading}
                  class="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                >
                  終了
                </button>
              </div>
            </div>
          </div>
        {/if}
      </div>

      <!-- 情報パネル -->
      <div class="bg-white rounded-lg shadow-md p-6 mt-6">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">CBT（認知行動療法）について</h3>
        <div class="grid md:grid-cols-2 gap-6">
          <div>
            <h4 class="font-medium text-gray-700 mb-2">CBTとは？</h4>
            <p class="text-gray-600 text-sm">
              認知行動療法は、思考の癖に気づき、よりバランスの取れた考え方を見つけるための心理療法です。
            </p>
          </div>
          <div>
            <h4 class="font-medium text-gray-700 mb-2">このセッションでは</h4>
            <ul class="text-gray-600 text-sm space-y-1">
              <li>• あなたの思考を整理します</li>
              <li>• 新しい視点を見つけるお手伝いをします</li>
              <li>• 診断や直接的なアドバイスはしません</li>
              <li>• セッション内容はジャーナルに保存されます</li>
              <li>• 完全無料で利用できます（AI料金なし）</li>
            </ul>
          </div>
        </div>
        
        <!-- 技術情報 -->
        <div class="mt-6 p-4 bg-blue-50 rounded-lg">
          <h4 class="font-medium text-blue-800 mb-2">技術情報</h4>
          <p class="text-blue-700 text-sm">
            このCBTシステムは、OpenAI APIを使用せず、独自のアルゴリズムで動作する完全無料版です。
            料金が発生することはありません。
          </p>
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  /* チャットエリアのスクロール位置を最下部に固定 */
  #chat-area {
    scroll-behavior: smooth;
  }
</style> 