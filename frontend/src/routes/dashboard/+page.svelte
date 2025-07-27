<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchAPI } from '$lib/api';
  import { goto } from '$app/navigation';

  let user: any = null;
  let journals: any[] = [];
  let moods: any[] = [];
  let usageStatus: any = null;
  let loading = true;

  onMount(() => {
    // localStorageからユーザー情報を取得
    const userStr = localStorage.getItem('user');
    if (!userStr) {
      goto('/login');
      return;
    }
    user = JSON.parse(userStr);
    loadData();
  });

  async function loadData() {
    try {
      // ジャーナルと気分記録を取得
      journals = await fetchAPI('/journals');
      moods = await fetchAPI('/moods');
      
      // 使用回数状況を取得
      usageStatus = await fetchAPI('/usage/status');
    } catch (err) {
      console.error('データの取得に失敗しました:', err);
    } finally {
      loading = false;
    }
  }

  function handleLogout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    goto('/');
  }

  function upgradePlan() {
    // プランアップグレード処理（実装予定）
    alert('プランアップグレード機能は準備中です');
  }

  function getUsageColor(percentage: number) {
    if (percentage >= 80) return 'text-red-600';
    if (percentage >= 60) return 'text-yellow-600';
    return 'text-green-600';
  }
</script>

<main class="min-h-screen bg-gray-50">
  <div class="max-w-4xl mx-auto p-6">
    <!-- ヘッダー -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">ダッシュボード</h1>
          <p class="text-gray-600">ようこそ、{user?.name || user?.email}さん</p>
        </div>
        <div class="flex gap-2">
          <a href="/" class="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-md text-sm">
            ホーム
          </a>
          <a href="/profile" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md text-sm">
            プロフィール
          </a>
          <button
            on:click={upgradePlan}
            class="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-md text-sm"
          >
            プランアップグレード
          </button>
          <button
            on:click={handleLogout}
            class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md text-sm"
          >
            ログアウト
          </button>
        </div>
      </div>
      
      <!-- プラン情報 -->
      <div class="mt-4 p-4 bg-blue-50 rounded-md">
        <h3 class="font-semibold text-blue-800">現在のプラン: {user?.plan_type === 'free' ? 'フリープラン' : 'プレミアムプラン'}</h3>
        {#if user?.plan_type === 'free'}
          <p class="text-sm text-blue-600 mt-1">機能に制限があります。プレミアムプランにアップグレードすると制限がなくなります。</p>
        {/if}
      </div>
    </div>

    {#if loading}
      <div class="text-center py-8">
        <p class="text-gray-600">読み込み中...</p>
      </div>
    {:else}
      <!-- 使用回数状況 -->
      {#if usageStatus}
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 class="text-xl font-bold mb-4 text-gray-800">使用回数状況</h2>
          <div class="grid md:grid-cols-3 gap-4">
            {#each Object.entries(usageStatus.usage) as [feature, data]}
              {@const usageData = data as any}
              <div class="p-4 border rounded-lg">
                <h3 class="font-semibold text-gray-700 mb-2">
                  {feature === 'journal' ? 'ジャーナル' : 
                   feature === 'mood' ? '気分記録' : 
                   feature === 'ai_analysis' ? 'AI分析' : 
                   feature === 'cbt_session' ? 'CBTセッション' : feature}
                </h3>
                <div class="space-y-2">
                  <div class="flex justify-between text-sm">
                    <span>使用回数:</span>
                    <span class="font-semibold {getUsageColor(usageData.percentage)}">
                      {usageData.current_usage} / {usageData.limit}
                    </span>
                  </div>
                  <div class="flex justify-between text-sm">
                    <span>残り:</span>
                    <span class="font-semibold">{usageData.remaining}回</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      class="h-2 rounded-full {usageData.percentage >= 80 ? 'bg-red-500' : usageData.percentage >= 60 ? 'bg-yellow-500' : 'bg-green-500'}" 
                      style="width: {Math.min(usageData.percentage, 100)}%"
                    ></div>
                  </div>
                </div>
              </div>
            {/each}
          </div>
        </div>
      {/if}

      <!-- 履歴セクション -->
      <div class="grid md:grid-cols-2 gap-6">
        <!-- ジャーナル履歴 -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-bold mb-4 text-blue-600">ジャーナル履歴</h2>
          {#if journals.length > 0}
            <div class="space-y-3">
              {#each journals.slice(0, 5) as journal}
                <div class="p-3 bg-blue-50 rounded-md">
                  <p class="text-sm text-gray-600">{new Date(journal.created_at).toLocaleDateString()}</p>
                  <p class="text-gray-800">{journal.content.substring(0, 100)}...</p>
                </div>
              {/each}
            </div>
            <div class="mt-4">
              <a href="/journals" class="text-blue-500 hover:text-blue-600 text-sm">すべて見る →</a>
            </div>
          {:else}
            <p class="text-gray-500">まだジャーナルがありません</p>
            <a href="/journals" class="text-blue-500 hover:text-blue-600 text-sm">ジャーナルを書く →</a>
          {/if}
        </div>

        <!-- 気分記録履歴 -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-bold mb-4 text-lime-600">気分記録履歴</h2>
          {#if moods.length > 0}
            <div class="space-y-3">
              {#each moods.slice(0, 5) as mood}
                <div class="p-3 bg-lime-50 rounded-md">
                  <p class="text-sm text-gray-600">{new Date(mood.recorded_at).toLocaleDateString()}</p>
                  <p class="text-gray-800">気分: {mood.mood}/5 {mood.note ? `(${mood.note})` : ''}</p>
                </div>
              {/each}
            </div>
            <div class="mt-4">
              <a href="/moods" class="text-lime-500 hover:text-lime-600 text-sm">すべて見る →</a>
            </div>
          {:else}
            <p class="text-gray-500">まだ気分記録がありません</p>
            <a href="/moods" class="text-lime-500 hover:text-lime-600 text-sm">気分を記録する →</a>
          {/if}
        </div>
      </div>

      <!-- クイックアクション -->
      <div class="mt-6 bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-bold mb-4 text-gray-800">クイックアクション</h2>
        <div class="flex gap-4 flex-wrap">
          <a href="/journals" class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-md font-semibold">
            ジャーナルを書く
          </a>
          <a href="/moods" class="bg-lime-500 hover:bg-lime-600 text-white px-6 py-3 rounded-md font-semibold">
            気分を記録
          </a>
          <a href="/cbt" class="bg-indigo-500 hover:bg-indigo-600 text-white px-6 py-3 rounded-md font-semibold">
            CBTセッション
          </a>
          <a href="/analysis" class="bg-purple-500 hover:bg-purple-600 text-white px-6 py-3 rounded-md font-semibold">
            AI分析
          </a>
          <a href="/meditation" class="bg-teal-500 hover:bg-teal-600 text-white px-6 py-3 rounded-md font-semibold">
            瞑想
          </a>
          <a href="/sounds" class="bg-pink-500 hover:bg-pink-600 text-white px-6 py-3 rounded-md font-semibold">
            サウンド
          </a>
          <a href="/pomodoro" class="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-md font-semibold">
            ポモドーロ
          </a>
        </div>
      </div>
    {/if}
  </div>
</main> 