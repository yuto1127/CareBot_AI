<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchAPI } from '$lib/api';

  type Mood = {
    id: number;
    user_id: number;
    mood: number;
    note?: string;
    recorded_at: string;
  };

  let moods: Mood[] = [];
  let user_id = 1; // テスト用
  let mood = 3;
  let note = '';
  let isLoggedIn = false;
  let error = '';
  let loading = false;

  onMount(() => {
    // ログイン状態をチェック
    const token = localStorage.getItem('token');
    isLoggedIn = !!token;
    loadMoods();
  });

  async function loadMoods() {
    moods = await fetchAPI('/moods');
  }

  async function addMood() {
    loading = true;
    error = '';
    
    try {
      await fetchAPI('/moods', {
        method: 'POST',
        body: JSON.stringify({ user_id, mood, note })
      });
      mood = 3;
      note = '';
      await loadMoods();
    } catch (err: any) {
      if (err.message && err.message.includes('使用回数制限')) {
        error = '使用回数制限に達しました。プレミアムプランにアップグレードしてください。';
      } else {
        error = '気分記録の追加に失敗しました。';
      }
    } finally {
      loading = false;
    }
  }

  async function deleteMood(id: number) {
    await fetchAPI(`/moods/${id}`, { method: 'DELETE' });
    await loadMoods();
  }
</script>

<div class="p-4">
  <div class="flex justify-between items-center mb-4">
    <a href="/" class="inline-block mb-4 bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded shadow">ホームに戻る</a>
    <div class="flex gap-2">
      {#if isLoggedIn}
        <a href="/dashboard" class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded shadow">ダッシュボード</a>
        <a href="/profile" class="bg-gray-500 hover:bg-gray-600 text-white font-semibold py-2 px-4 rounded shadow">プロフィール</a>
      {:else}
        <a href="/login" class="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded shadow">ログイン</a>
        <a href="/register" class="bg-orange-500 hover:bg-orange-600 text-white font-semibold py-2 px-4 rounded shadow">新規登録</a>
      {/if}
    </div>
  </div>

  <h2 class="text-xl font-bold mb-2">気分記録一覧</h2>
  <ul class="mb-4">
    {#each moods as m}
      <li class="mb-2 p-2 bg-lime-50 rounded flex items-center justify-between">
        <span>user_id: {m.user_id} | 気分: <strong>{m.mood}</strong> | {m.note}</span>
        <button class="ml-2 text-red-500" on:click={() => deleteMood(m.id)}>削除</button>
      </li>
    {/each}
  </ul>

  <h3 class="font-semibold mb-1">新規気分記録追加</h3>
  
  {#if error}
    <div class="mb-4 p-3 bg-red-100 text-red-700 rounded">
      {error}
      {#if error.includes('使用回数制限')}
        <div class="mt-2">
          <a href="/dashboard" class="text-blue-600 hover:text-blue-800 underline">プランアップグレード</a>
        </div>
      {/if}
    </div>
  {/if}
  
  <div class="flex gap-2 mb-4 items-center">
    <input 
      class="border rounded px-2 py-1 w-16" 
      type="number" 
      min="1" 
      max="5" 
      bind:value={mood} 
      placeholder="気分(1-5)" 
      disabled={loading}
    />
    <input 
      class="border rounded px-2 py-1 flex-1" 
      bind:value={note} 
      placeholder="メモ" 
      disabled={loading}
    />
    <button 
      class="bg-lime-400 text-white px-3 py-1 rounded disabled:bg-gray-400" 
      on:click={addMood}
      disabled={loading}
    >
      {loading ? '追加中...' : '追加'}
    </button>
  </div>
</div> 