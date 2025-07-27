<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchAPI } from '$lib/api';
  
  let sessions: any[] = [];
  let recommendations: any[] = [];
  let categories: any = {};
  let loading = false;
  let error = '';
  let isLoggedIn = false;
  let selectedCategory = '';
  let currentSession: any = null;
  let isPlaying = false;
  let currentTime = 0;
  let totalDuration = 0;
  let audio: HTMLAudioElement | null = null;
  
  onMount(async () => {
    // ログイン状態チェック
    const user = localStorage.getItem('user');
    if (!user) {
      isLoggedIn = false;
      return;
    }
    isLoggedIn = true;
    
    await loadData();
  });
  
  async function loadData() {
    loading = true;
    error = '';
    
    try {
      // セッション一覧を取得
      const sessionsResponse = await fetchAPI('/meditation/sessions');
      sessions = sessionsResponse.sessions;
      
      // 推奨セッションを取得
      const recommendationsResponse = await fetchAPI('/meditation/recommendations');
      recommendations = recommendationsResponse.recommendations;
      
      // カテゴリ一覧を取得
      const categoriesResponse = await fetchAPI('/meditation/categories');
      categories = categoriesResponse.categories;
      
    } catch (err: any) {
      error = 'データの取得に失敗しました: ' + (err.message || '不明なエラー');
    } finally {
      loading = false;
    }
  }
  
  async function startSession(sessionId: string) {
    if (!isLoggedIn) return;
    
    loading = true;
    error = '';
    
    try {
      const response = await fetchAPI(`/meditation/sessions/${sessionId}/start`, {
        method: 'POST'
      });
      
      currentSession = response.session_data;
      totalDuration = currentSession.duration;
      currentTime = 0;
      isPlaying = true;
      
      // 音声再生をシミュレート（実際の実装では音声ファイルを使用）
      simulateAudioPlayback();
      
    } catch (err: any) {
      if (err.status === 429) {
        error = '瞑想セッションの使用回数上限に達しました。プレミアムプランへのアップグレードをご検討ください。';
      } else {
        error = 'セッション開始に失敗しました: ' + (err.message || '不明なエラー');
      }
    } finally {
      loading = false;
    }
  }
  
  function simulateAudioPlayback() {
    // 実際の実装では音声ファイルを再生
    // ここではタイマーでシミュレート
    const timer = setInterval(() => {
      if (isPlaying && currentTime < totalDuration) {
        currentTime += 1;
      } else {
        clearInterval(timer);
        if (currentTime >= totalDuration) {
          completeSession();
        }
      }
    }, 1000);
  }
  
  async function completeSession() {
    if (!currentSession) return;
    
    try {
      await fetchAPI(`/meditation/sessions/${currentSession.session_id}/complete`, {
        method: 'POST'
      });
      
      isPlaying = false;
      currentSession = null;
      currentTime = 0;
      
    } catch (err: any) {
      error = 'セッション完了に失敗しました: ' + (err.message || '不明なエラー');
    }
  }
  
  function pauseSession() {
    isPlaying = false;
  }
  
  function resumeSession() {
    isPlaying = true;
    simulateAudioPlayback();
  }
  
  function stopSession() {
    isPlaying = false;
    currentSession = null;
    currentTime = 0;
  }
  
  function formatTime(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
  
  function filterSessionsByCategory(category: string) {
    selectedCategory = category;
  }
  
  function getFilteredSessions() {
    if (!selectedCategory) return sessions;
    return sessions.filter(session => session.category === selectedCategory);
  }
</script>

<svelte:head>
  <title>瞑想・マインドフルネス - CareBot AI</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-green-50 to-blue-100 p-4">
  <div class="max-w-6xl mx-auto">
    <!-- ヘッダー -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">🧘‍♀️ 瞑想・マインドフルネス</h1>
          <p class="text-gray-600 mt-2">
            心を落ち着かせ、内なる平安を見つけるためのガイド付き瞑想セッション
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
          瞑想セッションを利用するには、アカウントにログインしてください。
        </p>
        <a href="/login" class="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors">
          ログインする
        </a>
      </div>
    {:else}
      <!-- 現在のセッション -->
      {#if currentSession}
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4">現在のセッション</h2>
          <div class="text-center">
            <h3 class="text-lg font-semibold text-gray-700 mb-2">{currentSession.title}</h3>
            <div class="text-3xl font-bold text-blue-600 mb-4">
              {formatTime(currentTime)} / {formatTime(totalDuration)}
            </div>
            <div class="w-full bg-gray-200 rounded-full h-3 mb-4">
              <div 
                class="bg-blue-500 h-3 rounded-full transition-all duration-1000" 
                style="width: {(currentTime / totalDuration) * 100}%"
              ></div>
            </div>
            <div class="flex justify-center gap-4">
              {#if isPlaying}
                <button
                  on:click={pauseSession}
                  class="bg-yellow-500 text-white px-6 py-2 rounded-lg hover:bg-yellow-600 transition-colors"
                >
                  一時停止
                </button>
              {:else}
                <button
                  on:click={resumeSession}
                  class="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600 transition-colors"
                >
                  再開
                </button>
              {/if}
              <button
                on:click={stopSession}
                class="bg-red-500 text-white px-6 py-2 rounded-lg hover:bg-red-600 transition-colors"
              >
                停止
              </button>
            </div>
          </div>
        </div>
      {/if}

      <!-- 推奨セッション -->
      {#if recommendations.length > 0}
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4">おすすめのセッション</h2>
          <div class="grid md:grid-cols-3 gap-4">
            {#each recommendations as session}
              <div class="border rounded-lg p-4 hover:shadow-md transition-shadow">
                <h3 class="font-semibold text-gray-800 mb-2">{session.title}</h3>
                <p class="text-sm text-gray-600 mb-3">{session.description}</p>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-500">{Math.floor(session.duration / 60)}分</span>
                  <button
                    on:click={() => startSession(session.id)}
                    disabled={loading}
                    class="bg-blue-500 text-white px-4 py-2 rounded text-sm hover:bg-blue-600 disabled:bg-gray-300 transition-colors"
                  >
                    開始
                  </button>
                </div>
              </div>
            {/each}
          </div>
        </div>
      {/if}

      <!-- カテゴリフィルター -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4">カテゴリ別</h2>
        <div class="flex gap-2 mb-4">
          <button
            on:click={() => filterSessionsByCategory('')}
            class="px-4 py-2 rounded-lg {!selectedCategory ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'} hover:bg-blue-600 hover:text-white transition-colors"
          >
            すべて
          </button>
          {#each Object.entries(categories) as [key, category]}
            <button
              on:click={() => filterSessionsByCategory(key)}
              class="px-4 py-2 rounded-lg {selectedCategory === key ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'} hover:bg-blue-600 hover:text-white transition-colors"
            >
              {category.name}
            </button>
          {/each}
        </div>
      </div>

      <!-- セッション一覧 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4">すべてのセッション</h2>
        {#if loading}
          <div class="text-center py-8">
            <p class="text-gray-600">読み込み中...</p>
          </div>
        {:else if error}
          <div class="bg-red-50 border-l-4 border-red-400 p-4">
            <p class="text-red-700">{error}</p>
          </div>
        {:else}
          <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {#each getFilteredSessions() as session}
              <div class="border rounded-lg p-4 hover:shadow-md transition-shadow">
                <h3 class="font-semibold text-gray-800 mb-2">{session.title}</h3>
                <p class="text-sm text-gray-600 mb-3">{session.description}</p>
                <div class="flex flex-wrap gap-1 mb-3">
                  {#each session.tags as tag}
                    <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">{tag}</span>
                  {/each}
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-500">{Math.floor(session.duration / 60)}分</span>
                  <button
                    on:click={() => startSession(session.id)}
                    disabled={loading}
                    class="bg-green-500 text-white px-4 py-2 rounded text-sm hover:bg-green-600 disabled:bg-gray-300 transition-colors"
                  >
                    開始
                  </button>
                </div>
              </div>
            {/each}
          </div>
        {/if}
      </div>
    {/if}
  </div>
</div> 