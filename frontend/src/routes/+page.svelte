<script lang="ts">
  import { onMount } from 'svelte';
  
  let isLoggedIn = false;
  let user: any = null;
  
  onMount(() => {
    // ログイン状態をチェック
    const userData = localStorage.getItem('user');
    if (userData) {
      try {
        user = JSON.parse(userData);
        isLoggedIn = true;
      } catch (e) {
        console.error('ユーザーデータの解析エラー:', e);
        localStorage.removeItem('user');
      }
    }
  });
  
  function logout() {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    isLoggedIn = false;
    user = null;
    // ページをリロードして状態を更新
    window.location.reload();
  }
</script>

<main class="min-h-screen flex flex-col items-center justify-center bg-white">
  <h1 class="text-3xl font-bold mb-6 text-blue-500">CareBot AI ホーム</h1>
  
  {#if isLoggedIn}
    <!-- ログイン済みユーザー向け -->
    <div class="text-center mb-8">
      <p class="text-gray-600 mb-2">ようこそ、{user?.username || 'ユーザー'}さん！</p>
      <p class="text-sm text-gray-500">メンタルウェルネスをサポートするAIアシスタント</p>
    </div>

    <!-- 機能ナビゲーション -->
    <nav class="grid grid-cols-2 md:grid-cols-3 gap-4 w-full max-w-4xl mb-8 px-4">
      <a href="/dashboard" class="block bg-blue-100 hover:bg-blue-200 text-blue-800 font-semibold py-4 px-6 rounded-lg shadow text-center transition-colors">
        <div class="text-2xl mb-2">📊</div>
        ダッシュボード
      </a>
      <a href="/journal" class="block bg-blue-100 hover:bg-blue-200 text-blue-800 font-semibold py-4 px-6 rounded-lg shadow text-center transition-colors">
        <div class="text-2xl mb-2">📝</div>
        ジャーナル
      </a>
      <a href="/mood" class="block bg-green-100 hover:bg-green-200 text-green-800 font-semibold py-4 px-6 rounded-lg shadow text-center transition-colors">
        <div class="text-2xl mb-2">😊</div>
        気分記録
      </a>
      <a href="/cbt" class="block bg-indigo-100 hover:bg-indigo-200 text-indigo-800 font-semibold py-4 px-6 rounded-lg shadow text-center transition-colors">
        <div class="text-2xl mb-2">🧠</div>
        CBTセッション
      </a>
      <a href="/analysis" class="block bg-purple-100 hover:bg-purple-200 text-purple-800 font-semibold py-4 px-6 rounded-lg shadow text-center transition-colors">
        <div class="text-2xl mb-2">🤖</div>
        AI分析
      </a>
      <a href="/meditation" class="block bg-teal-100 hover:bg-teal-200 text-teal-800 font-semibold py-4 px-6 rounded-lg shadow text-center transition-colors">
        <div class="text-2xl mb-2">🧘‍♀️</div>
        瞑想
      </a>
      <a href="/sounds" class="block bg-pink-100 hover:bg-pink-200 text-pink-800 font-semibold py-4 px-6 rounded-lg shadow text-center transition-colors">
        <div class="text-2xl mb-2">🎵</div>
        リラックスサウンド
      </a>
      <a href="/pomodoro" class="block bg-orange-100 hover:bg-orange-200 text-orange-800 font-semibold py-4 px-6 rounded-lg shadow text-center transition-colors">
        <div class="text-2xl mb-2">⏰</div>
        ポモドーロタイマー
      </a>
    </nav>

    <!-- ユーザーアクション -->
    <div class="flex gap-4">
      <a href="/profile" class="bg-gray-500 hover:bg-gray-600 text-white font-semibold py-2 px-6 rounded shadow transition-colors">
        プロフィール
      </a>
      <button 
        on:click={logout}
        class="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-6 rounded shadow transition-colors"
      >
        ログアウト
      </button>
    </div>
  {:else}
    <!-- 未ログインユーザー向け -->
    <div class="text-center mb-8">
      <p class="text-gray-600 mb-4">メンタルウェルネスをサポートするAIアシスタント</p>
      <p class="text-sm text-gray-500">ログインしなくてもお試し機能をご利用いただけます</p>
    </div>

    <!-- お試し機能ナビゲーション -->
    <nav class="flex flex-col gap-4 w-full max-w-xs mb-8">
      <a href="/journal" class="block bg-blue-100 hover:bg-blue-200 text-blue-800 font-semibold py-3 px-6 rounded shadow text-center transition-colors">
        ジャーナルを書く（お試し）
      </a>
      <a href="/mood" class="block bg-lime-100 hover:bg-lime-200 text-lime-800 font-semibold py-3 px-6 rounded shadow text-center transition-colors">
        気分を記録（お試し）
      </a>
      <a href="/cbt" class="block bg-indigo-100 hover:bg-indigo-200 text-indigo-800 font-semibold py-3 px-6 rounded shadow text-center transition-colors">
        CBTセッション（ログイン必要）
      </a>
      <a href="/analysis" class="block bg-purple-100 hover:bg-purple-200 text-purple-800 font-semibold py-3 px-6 rounded shadow text-center transition-colors">
        AI分析（ログイン必要）
      </a>
    </nav>

    <!-- ログイン・新規登録ボタン -->
    <div class="flex gap-4">
      <a href="/login" class="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-6 rounded shadow transition-colors">
        ログイン
      </a>
      <a href="/register" class="bg-orange-500 hover:bg-orange-600 text-white font-semibold py-2 px-6 rounded shadow transition-colors">
        新規登録
      </a>
    </div>
  {/if}
</main>
