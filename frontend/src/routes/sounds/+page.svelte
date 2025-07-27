<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchAPI } from '$lib/api';
  
  let sounds: any[] = [];
  let categories: any = {};
  let presets: any = {};
  let recommendations: any[] = [];
  let loading = false;
  let error = '';
  let isLoggedIn = false;
  let selectedCategory = '';
  let selectedPreset = '';
  let currentSoundscape: any = null;
  let isPlaying = false;
  let volume = 0.5;
  
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
      // サウンド一覧を取得
      const soundsResponse = await fetchAPI('/sounds/');
      sounds = soundsResponse.sounds;
      
      // カテゴリ一覧を取得
      const categoriesResponse = await fetchAPI('/sounds/categories');
      categories = categoriesResponse.categories;
      
      // プリセット一覧を取得
      const presetsResponse = await fetchAPI('/sounds/presets');
      presets = presetsResponse.presets;
      
      // 推奨サウンドを取得
      const recommendationsResponse = await fetchAPI('/sounds/recommendations');
      recommendations = recommendationsResponse.recommendations;
      
    } catch (err: any) {
      error = 'データの取得に失敗しました: ' + (err.message || '不明なエラー');
    } finally {
      loading = false;
    }
  }
  
  async function playSound(soundId: string) {
    if (!isLoggedIn) return;
    
    loading = true;
    error = '';
    
    try {
      const response = await fetchAPI('/sounds/play', {
        method: 'POST',
        body: JSON.stringify({ sound_id: soundId, volume: volume })
      });
      
      // 実際の実装では音声ファイルを再生
      console.log('Playing sound:', response.sound);
      
    } catch (err: any) {
      if (err.status === 429) {
        error = 'サウンド再生の使用回数上限に達しました。プレミアムプランへのアップグレードをご検討ください。';
      } else {
        error = 'サウンド再生に失敗しました: ' + (err.message || '不明なエラー');
      }
    } finally {
      loading = false;
    }
  }
  
  async function createCustomSoundscape(soundIds: string[], volumes: number[]) {
    if (!isLoggedIn) return;
    
    try {
      const response = await fetchAPI('/sounds/create-soundscape', {
        method: 'POST',
        body: JSON.stringify({ sound_ids: soundIds, volumes: volumes })
      });
      
      currentSoundscape = response.soundscape;
      
    } catch (err: any) {
      error = 'サウンドスケープ作成に失敗しました: ' + (err.message || '不明なエラー');
    }
  }
  
  async function saveFavorite(soundscape: any) {
    if (!isLoggedIn) return;
    
    try {
      await fetchAPI('/sounds/favorites', {
        method: 'POST',
        body: JSON.stringify(soundscape)
      });
      
      // 成功メッセージを表示
      console.log('お気に入りに保存しました');
      
    } catch (err: any) {
      error = 'お気に入り保存に失敗しました: ' + (err.message || '不明なエラー');
    }
  }
  
  function filterSoundsByCategory(category: string) {
    selectedCategory = category;
  }
  
  function getFilteredSounds() {
    if (!selectedCategory) return sounds;
    return sounds.filter(sound => sound.category === selectedCategory);
  }
  
  function getPresetSounds(presetId: string) {
    const preset = presets[presetId];
    if (!preset) return [];
    
    return preset.sounds.map((soundRef: any) => {
      const sound = sounds.find(s => s.id === soundRef.id);
      return {
        ...sound,
        volume: soundRef.volume
      };
    });
  }
</script>

<svelte:head>
  <title>リラックスサウンド - CareBot AI</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100 p-4">
  <div class="max-w-6xl mx-auto">
    <!-- ヘッダー -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">🎵 リラックスサウンド</h1>
          <p class="text-gray-600 mt-2">
            集中、リラックス、睡眠のための環境音と音楽ライブラリ
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
          リラックスサウンドを利用するには、アカウントにログインしてください。
        </p>
        <a href="/login" class="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors">
          ログインする
        </a>
      </div>
    {:else}
      <!-- 推奨サウンド -->
      {#if recommendations.length > 0}
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4">おすすめのサウンド</h2>
          <div class="grid md:grid-cols-3 gap-4">
            {#each recommendations as sound}
              <div class="border rounded-lg p-4 hover:shadow-md transition-shadow">
                <h3 class="font-semibold text-gray-800 mb-2">{sound.name}</h3>
                <p class="text-sm text-gray-600 mb-3">{sound.description}</p>
                <div class="flex flex-wrap gap-1 mb-3">
                  {#each sound.tags as tag}
                    <span class="bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded">{tag}</span>
                  {/each}
                </div>
                <button
                  on:click={() => playSound(sound.id)}
                  disabled={loading}
                  class="w-full bg-purple-500 text-white px-4 py-2 rounded text-sm hover:bg-purple-600 disabled:bg-gray-300 transition-colors"
                >
                  再生
                </button>
              </div>
            {/each}
          </div>
        </div>
      {/if}

      <!-- プリセットサウンドスケープ -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4">プリセットサウンドスケープ</h2>
        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
          {#each Object.entries(presets) as [presetId, preset]}
            <div class="border rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-semibold text-gray-800 mb-2">{preset.name}</h3>
              <p class="text-sm text-gray-600 mb-3">{preset.description}</p>
              <div class="text-xs text-gray-500 mb-3">
                含まれるサウンド: {preset.sounds.length}個
              </div>
              <button
                on:click={() => createCustomSoundscape(preset.sounds.map((s: any) => s.id), preset.sounds.map((s: any) => s.volume))}
                disabled={loading}
                class="w-full bg-indigo-500 text-white px-4 py-2 rounded text-sm hover:bg-indigo-600 disabled:bg-gray-300 transition-colors"
              >
                作成
              </button>
            </div>
          {/each}
        </div>
      </div>

      <!-- カテゴリフィルター -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4">カテゴリ別</h2>
        <div class="flex gap-2 mb-4">
          <button
            on:click={() => filterSoundsByCategory('')}
            class="px-4 py-2 rounded-lg {!selectedCategory ? 'bg-purple-500 text-white' : 'bg-gray-200 text-gray-700'} hover:bg-purple-600 hover:text-white transition-colors"
          >
            すべて
          </button>
          {#each Object.entries(categories) as [key, category]}
            <button
              on:click={() => filterSoundsByCategory(key)}
              class="px-4 py-2 rounded-lg {selectedCategory === key ? 'bg-purple-500 text-white' : 'bg-gray-200 text-gray-700'} hover:bg-purple-600 hover:text-white transition-colors"
            >
              {category.name}
            </button>
          {/each}
        </div>
      </div>

      <!-- サウンド一覧 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4">すべてのサウンド</h2>
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
            {#each getFilteredSounds() as sound}
              <div class="border rounded-lg p-4 hover:shadow-md transition-shadow">
                <h3 class="font-semibold text-gray-800 mb-2">{sound.name}</h3>
                <p class="text-sm text-gray-600 mb-3">{sound.description}</p>
                <div class="flex flex-wrap gap-1 mb-3">
                  {#each sound.tags as tag}
                    <span class="bg-indigo-100 text-indigo-800 text-xs px-2 py-1 rounded">{tag}</span>
                  {/each}
                </div>
                <div class="flex items-center gap-2 mb-3">
                  <span class="text-xs text-gray-500">ボリューム:</span>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    bind:value={volume}
                    class="flex-1"
                  />
                  <span class="text-xs text-gray-500">{Math.round(volume * 100)}%</span>
                </div>
                <button
                  on:click={() => playSound(sound.id)}
                  disabled={loading}
                  class="w-full bg-green-500 text-white px-4 py-2 rounded text-sm hover:bg-green-600 disabled:bg-gray-300 transition-colors"
                >
                  再生
                </button>
              </div>
            {/each}
          </div>
        {/if}
      </div>

      <!-- 現在のサウンドスケープ -->
      {#if currentSoundscape}
        <div class="bg-white rounded-lg shadow-md p-6 mt-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4">現在のサウンドスケープ</h2>
          <div class="border rounded-lg p-4">
            <h3 class="font-semibold text-gray-800 mb-2">{currentSoundscape.name}</h3>
            <p class="text-sm text-gray-600 mb-3">{currentSoundscape.description}</p>
            <div class="space-y-2 mb-4">
              {#each currentSoundscape.sounds as sound}
                <div class="flex justify-between items-center">
                  <span class="text-sm">{sound.name}</span>
                  <span class="text-xs text-gray-500">{Math.round(sound.volume * 100)}%</span>
                </div>
              {/each}
            </div>
            <div class="flex gap-2">
              <button
                on:click={() => saveFavorite(currentSoundscape)}
                class="bg-blue-500 text-white px-4 py-2 rounded text-sm hover:bg-blue-600 transition-colors"
              >
                お気に入りに保存
              </button>
              <button
                on:click={() => currentSoundscape = null}
                class="bg-gray-500 text-white px-4 py-2 rounded text-sm hover:bg-gray-600 transition-colors"
              >
                閉じる
              </button>
            </div>
          </div>
        </div>
      {/if}
    {/if}
  </div>
</div> 