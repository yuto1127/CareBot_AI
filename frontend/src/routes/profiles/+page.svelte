<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchAPI } from '$lib/api';

  type Profile = {
    id: number;
    user_id: number;
    display_name?: string;
    avatar_url?: string;
    bio?: string;
    created_at: string;
  };

  let profiles: Profile[] = [];
  let user_id = 1; // テスト用
  let display_name = '';
  let avatar_url = '';
  let bio = '';

  async function loadProfiles() {
    profiles = await fetchAPI('/profiles');
  }

  async function addProfile() {
    await fetchAPI('/profiles', {
      method: 'POST',
      body: JSON.stringify({ user_id, display_name, avatar_url, bio })
    });
    display_name = '';
    avatar_url = '';
    bio = '';
    await loadProfiles();
  }

  async function deleteProfile(id: number) {
    await fetchAPI(`/profiles/${id}`, { method: 'DELETE' });
    await loadProfiles();
  }

  onMount(loadProfiles);
</script>

<a href="/" class="inline-block mb-4 bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded shadow">ホームに戻る</a>

<h2 class="text-xl font-bold mb-2">プロフィール一覧</h2>
<ul class="mb-4">
  {#each profiles as p}
    <li class="mb-2 p-2 bg-orange-50 rounded flex items-center justify-between">
      <span><strong>{p.display_name}</strong>（user_id: {p.user_id}）</span>
      <button class="ml-2 text-red-500" on:click={() => deleteProfile(p.id)}>削除</button>
    </li>
  {/each}
</ul>

<h3 class="font-semibold mb-1">新規プロフィール追加</h3>
<div class="flex gap-2 mb-4">
  <input class="border rounded px-2 py-1 flex-1" bind:value={display_name} placeholder="表示名" />
  <input class="border rounded px-2 py-1 flex-1" bind:value={avatar_url} placeholder="アバターURL" />
  <input class="border rounded px-2 py-1 flex-1" bind:value={bio} placeholder="自己紹介" />
  <button class="bg-orange-400 text-white px-3 py-1 rounded" on:click={addProfile}>追加</button>
</div> 