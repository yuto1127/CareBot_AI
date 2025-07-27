<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchAPI } from '$lib/api';
  
  let sessionData: any = null;
  let progress: any = null;
  let settings: any = {};
  let statistics: any = {};
  let loading = false;
  let error = '';
  let isLoggedIn = false;
  let isRunning = false;
  let timer: any = null;
  
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
      // デフォルト設定を取得
      const settingsResponse = await fetchAPI('/pomodoro/settings/default');
      settings = settingsResponse.settings;
      
      // 統計を取得
      const statisticsResponse = await fetchAPI('/pomodoro/statistics');
      statistics = statisticsResponse.statistics;
      
    } catch (err: any) {
      error = 'データの取得に失敗しました: ' + (err.message || '不明なエラー');
    } finally {
      loading = false;
    }
  }
  
  async function createSession() {
    if (!isLoggedIn) return;
    
    loading = true;
    error = '';
    
    try {
      const response = await fetchAPI('/pomodoro/session/create', {
        method: 'POST',
        body: JSON.stringify({ settings: settings })
      });
      
      sessionData = response.session_data;
      
    } catch (err: any) {
      error = 'セッション作成に失敗しました: ' + (err.message || '不明なエラー');
    } finally {
      loading = false;
    }
  }
  
  async function startFocusSession() {
    if (!sessionData) return;
    
    loading = true;
    error = '';
    
    try {
      const response = await fetchAPI('/pomodoro/session/start-focus', {
        method: 'POST',
        body: JSON.stringify(sessionData)
      });
      
      sessionData = response.session_data;
      isRunning = true;
      
      // タイマーを開始
      startTimer();
      
    } catch (err: any) {
      if (err.status === 429) {
        error = 'ポモドーロセッションの使用回数上限に達しました。プレミアムプランへのアップグレードをご検討ください。';
      } else {
        error = '集中セッション開始に失敗しました: ' + (err.message || '不明なエラー');
      }
    } finally {
      loading = false;
    }
  }
  
  async function startBreakSession() {
    if (!sessionData) return;
    
    loading = true;
    error = '';
    
    try {
      const response = await fetchAPI('/pomodoro/session/start-break', {
        method: 'POST',
        body: JSON.stringify(sessionData)
      });
      
      sessionData = response.session_data;
      isRunning = true;
      
      // タイマーを開始
      startTimer();
      
    } catch (err: any) {
      error = '休憩セッション開始に失敗しました: ' + (err.message || '不明なエラー');
    } finally {
      loading = false;
    }
  }
  
  async function pauseSession() {
    if (!sessionData) return;
    
    try {
      const response = await fetchAPI('/pomodoro/session/pause', {
        method: 'POST',
        body: JSON.stringify(sessionData)
      });
      
      sessionData = response.session_data;
      isRunning = false;
      
      // タイマーを停止
      if (timer) {
        clearInterval(timer);
        timer = null;
      }
      
    } catch (err: any) {
      error = 'セッション一時停止に失敗しました: ' + (err.message || '不明なエラー');
    }
  }
  
  async function resumeSession() {
    if (!sessionData) return;
    
    try {
      const response = await fetchAPI('/pomodoro/session/resume', {
        method: 'POST',
        body: JSON.stringify(sessionData)
      });
      
      sessionData = response.session_data;
      isRunning = true;
      
      // タイマーを再開
      startTimer();
      
    } catch (err: any) {
      error = 'セッション再開に失敗しました: ' + (err.message || '不明なエラー');
    }
  }
  
  async function completeSession() {
    if (!sessionData) return;
    
    try {
      const response = await fetchAPI('/pomodoro/session/complete', {
        method: 'POST',
        body: JSON.stringify(sessionData)
      });
      
      // タイマーを停止
      if (timer) {
        clearInterval(timer);
        timer = null;
      }
      
      isRunning = false;
      sessionData = null;
      progress = null;
      
      // 統計を更新
      await loadData();
      
    } catch (err: any) {
      error = 'セッション完了に失敗しました: ' + (err.message || '不明なエラー');
    }
  }
  
  function startTimer() {
    if (timer) {
      clearInterval(timer);
    }
    
    timer = setInterval(async () => {
      if (!sessionData) return;
      
      try {
        const response = await fetchAPI('/pomodoro/session/progress', {
          method: 'POST',
          body: JSON.stringify(sessionData)
        });
        
        progress = response.progress;
        sessionData = response.session_data;
        
        // セッションが完了した場合
        if (progress.remaining_time <= 0) {
          clearInterval(timer);
          timer = null;
          isRunning = false;
          
          // 自動的に次のセッションに進むか、完了する
          if (progress.cycle % 2 === 1) {
            // 集中セッション完了後は休憩へ
            await startBreakSession();
          } else {
            // 休憩完了後は完了
            await completeSession();
          }
        }
        
      } catch (err: any) {
        console.error('タイマー更新エラー:', err);
      }
    }, 1000);
  }
  
  function formatTime(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
  
  function getStateText(state: string): string {
    switch (state) {
      case 'focus': return '集中中';
      case 'break': return '休憩中';
      case 'long_break': return '長い休憩中';
      case 'paused': return '一時停止中';
      default: return '待機中';
    }
  }
  
  function getStateColor(state: string): string {
    switch (state) {
      case 'focus': return 'bg-red-500';
      case 'break': return 'bg-green-500';
      case 'long_break': return 'bg-blue-500';
      case 'paused': return 'bg-yellow-500';
      default: return 'bg-gray-500';
    }
  }
</script>

<svelte:head>
  <title>ポモドーロタイマー - CareBot AI</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-orange-50 to-red-100 p-4">
  <div class="max-w-4xl mx-auto">
    <!-- ヘッダー -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">⏰ ポモドーロタイマー</h1>
          <p class="text-gray-600 mt-2">
            25分の集中と5分の休憩で生産性を最大化する時間管理ツール
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
          ポモドーロタイマーを利用するには、アカウントにログインしてください。
        </p>
        <a href="/login" class="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors">
          ログインする
        </a>
      </div>
    {:else}
      <!-- メインタイマー -->
      <div class="bg-white rounded-lg shadow-md p-8 mb-6">
        <div class="text-center">
          {#if !sessionData}
            <!-- セッション未開始 -->
            <div class="text-6xl mb-6">⏰</div>
            <h2 class="text-2xl font-bold text-gray-800 mb-4">ポモドーロセッションを開始</h2>
            <p class="text-gray-600 mb-6">
              集中と休憩のサイクルで効率的に作業を進めましょう
            </p>
            <button
              on:click={createSession}
              disabled={loading}
              class="bg-red-500 text-white px-8 py-3 rounded-lg text-lg hover:bg-red-600 disabled:bg-gray-300 transition-colors"
            >
              {loading ? '作成中...' : 'セッションを作成'}
            </button>
          {:else if !isRunning}
            <!-- セッション待機中 -->
            <div class="text-6xl mb-6">🎯</div>
            <h2 class="text-2xl font-bold text-gray-800 mb-4">セッション準備完了</h2>
            <p class="text-gray-600 mb-6">
              サイクル {sessionData.current_cycle + 1} を開始します
            </p>
            <div class="flex justify-center gap-4">
              <button
                on:click={startFocusSession}
                disabled={loading}
                class="bg-red-500 text-white px-6 py-3 rounded-lg hover:bg-red-600 disabled:bg-gray-300 transition-colors"
              >
                {loading ? '開始中...' : '集中開始'}
              </button>
              <button
                on:click={startBreakSession}
                disabled={loading}
                class="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 disabled:bg-gray-300 transition-colors"
              >
                {loading ? '開始中...' : '休憩開始'}
              </button>
            </div>
          {:else}
            <!-- タイマー実行中 -->
            <div class="mb-6">
              <div class="text-8xl font-bold text-gray-800 mb-4">
                {progress ? formatTime(progress.remaining_time) : '00:00'}
              </div>
              <div class="flex justify-center items-center gap-2 mb-4">
                <div class="w-4 h-4 rounded-full {getStateColor(progress?.state || 'idle')}"></div>
                <span class="text-lg font-semibold text-gray-700">
                  {progress ? getStateText(progress.state) : '待機中'}
                </span>
              </div>
              <div class="text-sm text-gray-600 mb-6">
                サイクル {progress?.cycle || 0} / 目標時間: {progress ? formatTime(progress.target_duration) : '00:00'}
              </div>
              
              <!-- プログレスバー -->
              <div class="w-full bg-gray-200 rounded-full h-3 mb-6">
                <div 
                  class="h-3 rounded-full transition-all duration-1000 {progress?.state === 'focus' ? 'bg-red-500' : 'bg-green-500'}" 
                  style="width: {progress ? (100 - (progress.remaining_time / progress.target_duration) * 100) : 0}%"
                ></div>
              </div>
              
              <!-- コントロールボタン -->
              <div class="flex justify-center gap-4">
                {#if progress?.state === 'paused'}
                  <button
                    on:click={resumeSession}
                    class="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition-colors"
                  >
                    再開
                  </button>
                {:else}
                  <button
                    on:click={pauseSession}
                    class="bg-yellow-500 text-white px-6 py-3 rounded-lg hover:bg-yellow-600 transition-colors"
                  >
                    一時停止
                  </button>
                {/if}
                <button
                  on:click={completeSession}
                  class="bg-gray-500 text-white px-6 py-3 rounded-lg hover:bg-gray-600 transition-colors"
                >
                  完了
                </button>
              </div>
            </div>
          {/if}
        </div>
      </div>

      <!-- 統計情報 -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4">統計情報</h2>
        <div class="grid md:grid-cols-3 gap-4">
          <div class="text-center p-4 bg-blue-50 rounded-lg">
            <div class="text-2xl font-bold text-blue-600">{statistics.total_sessions || 0}</div>
            <div class="text-sm text-gray-600">総セッション数</div>
          </div>
          <div class="text-center p-4 bg-green-50 rounded-lg">
            <div class="text-2xl font-bold text-green-600">{Math.floor((statistics.total_focus_time || 0) / 60)}分</div>
            <div class="text-sm text-gray-600">総集中時間</div>
          </div>
          <div class="text-center p-4 bg-purple-50 rounded-lg">
            <div class="text-2xl font-bold text-purple-600">{statistics.total_cycles || 0}</div>
            <div class="text-sm text-gray-600">総サイクル数</div>
          </div>
        </div>
      </div>

      <!-- 設定 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4">タイマー設定</h2>
        <div class="grid md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">集中時間</label>
            <input
              type="number"
              bind:value={settings.focus_duration}
              min="60"
              max="3600"
              step="60"
              class="w-full p-2 border border-gray-300 rounded-lg"
            />
            <p class="text-xs text-gray-500 mt-1">秒単位（デフォルト: 1500秒 = 25分）</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">休憩時間</label>
            <input
              type="number"
              bind:value={settings.break_duration}
              min="60"
              max="1800"
              step="60"
              class="w-full p-2 border border-gray-300 rounded-lg"
            />
            <p class="text-xs text-gray-500 mt-1">秒単位（デフォルト: 300秒 = 5分）</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">長い休憩時間</label>
            <input
              type="number"
              bind:value={settings.long_break_duration}
              min="300"
              max="3600"
              step="60"
              class="w-full p-2 border border-gray-300 rounded-lg"
            />
            <p class="text-xs text-gray-500 mt-1">秒単位（デフォルト: 900秒 = 15分）</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">長い休憩までのサイクル数</label>
            <input
              type="number"
              bind:value={settings.cycles_before_long_break}
              min="1"
              max="10"
              step="1"
              class="w-full p-2 border border-gray-300 rounded-lg"
            />
            <p class="text-xs text-gray-500 mt-1">デフォルト: 4サイクル</p>
          </div>
        </div>
      </div>

      <!-- エラーメッセージ -->
      {#if error}
        <div class="bg-red-50 border-l-4 border-red-400 p-4 mt-6">
          <p class="text-red-700">{error}</p>
        </div>
      {/if}
    {/if}
  </div>
</div> 