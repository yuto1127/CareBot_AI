<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchAPI } from '$lib/api';

  type Journal = {
    id: number;
    user_id: number;
    content: string;
    created_at: string;
  };

  let journals: Journal[] = [];
  let content = '';
  let user_id = 1; // テスト用。実際はログインユーザーIDを使う
  let isLoggedIn = false;
  let error = '';
  let loading = false;

  onMount(() => {
    // ログイン状態をチェック
    const token = localStorage.getItem('token');
    isLoggedIn = !!token;
    loadJournals();
  });

  async function loadJournals() {
    journals = await fetchAPI('/journals');
  }

  async function addJournal() {
    if (!content.trim()) return;
    
    loading = true;
    error = '';
    
    try {
      await fetchAPI('/journals', {
        method: 'POST',
        body: JSON.stringify({ user_id, content })
      });
      content = '';
      await loadJournals();
    } catch (err: any) {
      if (err.message && err.message.includes('使用回数制限')) {
        error = '使用回数制限に達しました。プレミアムプランにアップグレードしてください。';
      } else {
        error = 'ジャーナルの追加に失敗しました。';
      }
    } finally {
      loading = false;
    }
  }

  async function deleteJournal(id: number) {
    await fetchAPI(`/journals/${id}`, { method: 'DELETE' });
    await loadJournals();
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

  <h2 class="text-xl font-bold mb-2">ジャーナル一覧</h2>
  <ul class="mb-4">
    {#each journals as j}
      <li class="mb-2 p-2 bg-blue-50 rounded flex items-center justify-between">
        <span><strong>{j.content}</strong>（{j.created_at}）</span>
        <button class="ml-2 text-red-500" on:click={() => deleteJournal(j.id)}>削除</button>
      </li>
    {/each}
  </ul>

  <h3 class="font-semibold mb-1">新規ジャーナル追加</h3>
  
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
  
  <div class="flex gap-2 mb-4">
    <input 
      class="border rounded px-2 py-1 flex-1" 
      bind:value={content} 
      placeholder="内容" 
      disabled={loading}
    />
    <button 
      class="bg-blue-400 text-white px-3 py-1 rounded disabled:bg-gray-400" 
      on:click={addJournal} 
      disabled={!content.trim() || loading}
    >
      {loading ? '追加中...' : '追加'}
    </button>
  </div>
</div> 