<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchAPI } from '$lib/api';

  type User = {
    id: number;
    email: string;
    name?: string;
    created_at: string;
  };

  let users: User[] = [];
  let email = '';
  let name = '';

  async function loadUsers() {
    users = await fetchAPI('/users');
  }

  async function addUser() {
    await fetchAPI('/users', {
      method: 'POST',
      body: JSON.stringify({ email, name })
    });
    email = '';
    name = '';
    await loadUsers();
  }

  async function deleteUser(id: number) {
    await fetchAPI(`/users/${id}`, { method: 'DELETE' });
    await loadUsers();
  }

  onMount(loadUsers);
</script>

<a href="/" class="inline-block mb-4 bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded shadow">ホームに戻る</a>

<h2 class="text-xl font-bold mb-2">ユーザー一覧</h2>
<ul class="mb-4">
  {#each users as u}
    <li class="mb-2 p-2 bg-green-50 rounded flex items-center justify-between">
      <span><strong>{u.email}</strong>（{u.name}）</span>
      <button class="ml-2 text-red-500" on:click={() => deleteUser(u.id)}>削除</button>
    </li>
  {/each}
</ul>

<h3 class="font-semibold mb-1">新規ユーザー追加</h3>
<div class="flex gap-2 mb-4">
  <input class="border rounded px-2 py-1 flex-1" bind:value={email} placeholder="メールアドレス" />
  <input class="border rounded px-2 py-1 flex-1" bind:value={name} placeholder="名前（任意）" />
  <button class="bg-green-400 text-white px-3 py-1 rounded" on:click={addUser} disabled={!email}>追加</button>
</div> 