<script lang="ts">
  import { fetchAPI } from '$lib/api';
  import { goto } from '$app/navigation';
  import { authStore } from '$lib/stores/auth';

  let email = '';
  let password = '';
  let error = '';
  let loading = false;

  async function handleLogin() {
    if (!email || !password) {
      error = 'メールアドレスとパスワードを入力してください';
      return;
    }

    loading = true;
    error = '';

    try {
      console.log('🔐 Attempting login with:', { email, password: '***' });
      
      const response = await fetchAPI('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      });

      console.log('✅ Login successful:', response);

      // ストアを使用してログイン状態を更新
      authStore.login(response.user);
      localStorage.setItem('token', response.access_token);
      
      console.log('💾 Login state updated via store');
      console.log('💾 User data:', response.user);
      console.log('💾 Token saved');

      // 少し待ってからダッシュボードへリダイレクト（状態更新を確実にするため）
      setTimeout(() => {
        goto('/dashboard');
      }, 100);
    } catch (err: any) {
      console.error('❌ Login failed:', err);
      error = `ログインに失敗しました: ${err.message}`;
    } finally {
      loading = false;
    }
  }
</script>

<main class="min-h-screen flex flex-col items-center justify-center bg-white">
  <div class="w-full max-w-md p-6 bg-white rounded-lg shadow-md">
    <h1 class="text-2xl font-bold text-center mb-6 text-blue-500">ログイン</h1>
    
    {#if error}
      <div class="mb-4 p-3 bg-red-100 text-red-700 rounded">
        {error}
      </div>
    {/if}

    <form on:submit|preventDefault={handleLogin} class="space-y-4">
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 mb-1">メールアドレス</label>
        <input
          id="email"
          type="email"
          bind:value={email}
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="example@email.com"
          required
        />
      </div>

      <div>
        <label for="password" class="block text-sm font-medium text-gray-700 mb-1">パスワード</label>
        <input
          id="password"
          type="password"
          bind:value={password}
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="パスワード"
          required
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        class="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-md transition-colors"
      >
        {loading ? 'ログイン中...' : 'ログイン'}
      </button>
    </form>

    <div class="mt-4 text-center">
      <p class="text-sm text-gray-600">
        アカウントをお持ちでない方は
        <a href="/register" class="text-blue-500 hover:text-blue-600">新規登録</a>
      </p>
    </div>

    <div class="mt-4 text-center">
      <a href="/" class="text-sm text-gray-500 hover:text-gray-700">ホームに戻る</a>
    </div>
    
    <!-- デバッグ情報（開発環境のみ） -->
    <div class="mt-6 p-4 bg-gray-100 rounded-lg">
      <h3 class="text-sm font-semibold text-gray-700 mb-2">デバッグ情報（テスト用）</h3>
      <div class="text-xs text-gray-600 space-y-1">
        <p><strong>テストユーザー:</strong> test@example.com</p>
        <p><strong>パスワード:</strong> Test1234</p>
        <p><strong>API URL:</strong> http://localhost:8000/api</p>
      </div>
    </div>
  </div>
</main> 