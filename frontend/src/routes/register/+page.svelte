<script lang="ts">
  import { fetchAPI } from '$lib/api';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';

  let email = '';
  let password = '';
  let name = '';
  let error = '';
  let loading = false;

  onMount(() => {
    // 法的・倫理的ポジショニングの同意確認
    const legalAgreement = localStorage.getItem('legal_agreement');
    if (!legalAgreement) {
      // 同意していない場合は法的・倫理的ポジショニングページにリダイレクト
      goto('/legal');
    }
  });

  async function handleRegister() {
    if (!email || !password) {
      error = 'メールアドレスとパスワードを入力してください';
      return;
    }

    loading = true;
    error = '';

    try {
      console.log('ユーザー登録を開始:', { email, name });
      
      // 法的・倫理的ポジショニングの同意確認を再送信
      const legalAgreement = localStorage.getItem('legal_agreement');
      if (legalAgreement) {
        await fetchAPI('/auth/legal-agreement', {
          method: 'POST',
          body: JSON.stringify({
            privacy_policy_agreed: true,
            terms_of_service_agreed: true,
            safety_guidelines_agreed: true
          })
        });
      }
      
      // ユーザー登録
      const registerResponse = await fetchAPI('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ email, password, name })
      });

      console.log('ユーザー登録成功:', registerResponse);

      // 登録成功後、自動ログイン
      console.log('自動ログインを開始:', { email });
      
      const loginResponse = await fetchAPI('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      });

      console.log('自動ログイン成功:', loginResponse);

      // トークンをlocalStorageに保存
      localStorage.setItem('token', loginResponse.access_token);
      localStorage.setItem('user', JSON.stringify(loginResponse.user));

      // ダッシュボードへリダイレクト
      goto('/dashboard');
    } catch (err: any) {
      console.error('登録エラー:', err);
      if (err.message && err.message.includes('既に登録されています')) {
        error = 'このメールアドレスは既に登録されています。';
      } else if (err.message && err.message.includes('パスワード')) {
        error = 'パスワードは8文字以上で、大文字・小文字・数字を含む必要があります。';
      } else if (err.message && err.message.includes('メールアドレス')) {
        error = '無効なメールアドレス形式です。';
      } else {
        error = '登録に失敗しました。もう一度お試しください。';
      }
    } finally {
      loading = false;
    }
  }
</script>

<main class="min-h-screen flex flex-col items-center justify-center bg-white">
  <div class="w-full max-w-md p-6 bg-white rounded-lg shadow-md">
    <h1 class="text-2xl font-bold text-center mb-6 text-blue-500">新規登録</h1>
    
    {#if error}
      <div class="mb-4 p-3 bg-red-100 text-red-700 rounded">
        {error}
      </div>
    {/if}

    <form on:submit|preventDefault={handleRegister} class="space-y-4">
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
          placeholder="パスワード（8文字以上、大文字・小文字・数字を含む）"
          required
        />
        <p class="text-xs text-gray-500 mt-1">パスワードは8文字以上で、大文字・小文字・数字を含む必要があります</p>
      </div>

      <div>
        <label for="name" class="block text-sm font-medium text-gray-700 mb-1">名前（任意）</label>
        <input
          id="name"
          type="text"
          bind:value={name}
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="お名前"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        class="w-full bg-orange-500 hover:bg-orange-600 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-md transition-colors"
      >
        {loading ? '登録中...' : '登録'}
      </button>
    </form>

    <div class="mt-4 text-center">
      <p class="text-sm text-gray-600">
        既にアカウントをお持ちの方は
        <a href="/login" class="text-blue-500 hover:text-blue-600">ログイン</a>
      </p>
    </div>

    <div class="mt-4 text-center">
      <a href="/" class="text-sm text-gray-500 hover:text-gray-700">ホームに戻る</a>
    </div>
  </div>
</main> 