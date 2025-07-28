<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  let user: any = null;
  let profile: any = null;
  let stats: any = null;
  let loading = true;
  let error = '';
  
  // フォーム状態
  let showEditForm = false;
  let editForm = {
    username: '',
    email: ''
  };
  
  // パスワード変更フォーム
  let showPasswordForm = false;
  let passwordForm = {
    current_password: '',
    new_password: '',
    confirm_password: ''
  };
  
  // アカウント削除フォーム
  let showDeleteForm = false;
  let deleteForm = {
    password: ''
  };
  
  onMount(async () => {
    const userData = localStorage.getItem('user');
    if (!userData) {
      goto('/login');
      return;
    }
    
    try {
      user = JSON.parse(userData);
      await loadProfile();
    } catch (e) {
      console.error('ユーザーデータの解析エラー:', e);
      goto('/login');
    }
  });
  
  async function loadProfile() {
    try {
      loading = true;
      const token = localStorage.getItem('token');
      
      const response = await fetch('http://localhost:8000/api/profiles/me/stats', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        profile = data.profile;
        stats = data.stats;
      } else {
        error = 'プロフィールの取得に失敗しました';
      }
    } catch (e) {
      error = 'ネットワークエラーが発生しました';
      console.error('プロフィール取得エラー:', e);
    } finally {
      loading = false;
    }
  }
  
  async function updateProfile() {
    try {
      const token = localStorage.getItem('token');
      const updateData: any = {};
      
      if (editForm.username) updateData.username = editForm.username;
      if (editForm.email) updateData.email = editForm.email;
      
      if (Object.keys(updateData).length === 0) {
        alert('更新するデータを入力してください');
        return;
      }
      
      const response = await fetch('http://localhost:8000/api/profiles/me', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updateData)
      });
      
      if (response.ok) {
        const data = await response.json();
        profile = data.profile;
        showEditForm = false;
        editForm = { username: '', email: '' };
        alert('プロフィールを更新しました');
      } else {
        const errorData = await response.json();
        alert(errorData.detail || 'プロフィールの更新に失敗しました');
      }
    } catch (e) {
      alert('ネットワークエラーが発生しました');
      console.error('プロフィール更新エラー:', e);
    }
  }
  
  async function changePassword() {
    if (passwordForm.new_password !== passwordForm.confirm_password) {
      alert('新しいパスワードが一致しません');
      return;
    }
    
    try {
      const token = localStorage.getItem('token');
      
      const response = await fetch('http://localhost:8000/api/profiles/me/change-password', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          current_password: passwordForm.current_password,
          new_password: passwordForm.new_password
        })
      });
      
      if (response.ok) {
        alert('パスワードを変更しました');
        showPasswordForm = false;
        passwordForm = { current_password: '', new_password: '', confirm_password: '' };
      } else {
        const errorData = await response.json();
        alert(errorData.detail || 'パスワードの変更に失敗しました');
      }
    } catch (e) {
      alert('ネットワークエラーが発生しました');
      console.error('パスワード変更エラー:', e);
    }
  }
  
  async function deleteAccount() {
    if (!confirm('本当にアカウントを削除しますか？この操作は取り消せません。')) {
      return;
    }
    
    try {
      const token = localStorage.getItem('token');
      
      const response = await fetch('http://localhost:8000/api/profiles/me', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          password: deleteForm.password
        })
      });
      
      if (response.ok) {
        alert('アカウントを削除しました');
        localStorage.removeItem('user');
        localStorage.removeItem('token');
        goto('/');
      } else {
        const errorData = await response.json();
        alert(errorData.detail || 'アカウントの削除に失敗しました');
      }
    } catch (e) {
      alert('ネットワークエラーが発生しました');
      console.error('アカウント削除エラー:', e);
    }
  }
  
  function logout() {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    goto('/');
  }
</script>

<main class="min-h-screen bg-gray-50 py-8">
  <div class="max-w-4xl mx-auto px-4">
    <!-- ヘッダー -->
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-gray-900">プロフィール</h1>
      <div class="flex gap-4">
        <a href="/dashboard" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded shadow">
          ダッシュボード
        </a>
        <button on:click={logout} class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded shadow">
          ログアウト
        </button>
      </div>
    </div>
    
    {#if loading}
      <div class="text-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
        <p class="mt-4 text-gray-600">読み込み中...</p>
      </div>
    {:else if error}
      <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
        {error}
      </div>
    {:else if profile}
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- プロフィール情報 -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-lg shadow p-6 mb-6">
            <h2 class="text-xl font-semibold mb-4">プロフィール情報</h2>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">ユーザー名</label>
                <p class="mt-1 text-gray-900">{profile.username}</p>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">メールアドレス</label>
                <p class="mt-1 text-gray-900">{profile.email}</p>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">プラン</label>
                <p class="mt-1 text-gray-900">{profile.plan_type === 'free' ? '無料プラン' : 'プレミアムプラン'}</p>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">登録日</label>
                <p class="mt-1 text-gray-900">{new Date(profile.created_at).toLocaleDateString('ja-JP')}</p>
              </div>
            </div>
            
            <button 
              on:click={() => showEditForm = !showEditForm}
              class="mt-4 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded shadow"
            >
              {showEditForm ? 'キャンセル' : 'プロフィールを編集'}
            </button>
          </div>
          
          <!-- 編集フォーム -->
          {#if showEditForm}
            <div class="bg-white rounded-lg shadow p-6 mb-6">
              <h3 class="text-lg font-semibold mb-4">プロフィール編集</h3>
              
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700">新しいユーザー名</label>
                  <input 
                    type="text" 
                    bind:value={editForm.username}
                    placeholder={profile.username}
                    class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700">新しいメールアドレス</label>
                  <input 
                    type="email" 
                    bind:value={editForm.email}
                    placeholder={profile.email}
                    class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
              
              <button 
                on:click={updateProfile}
                class="mt-4 bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded shadow"
              >
                更新
              </button>
            </div>
          {/if}
        </div>
        
        <!-- 統計情報 -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow p-6 mb-6">
            <h2 class="text-xl font-semibold mb-4">統計情報</h2>
            
            {#if stats}
              <div class="space-y-3">
                <div class="flex justify-between">
                  <span class="text-gray-600">ジャーナル数</span>
                  <span class="font-semibold">{stats.total_journals}</span>
                </div>
                
                <div class="flex justify-between">
                  <span class="text-gray-600">気分記録数</span>
                  <span class="font-semibold">{stats.total_moods}</span>
                </div>
                
                <div class="flex justify-between">
                  <span class="text-gray-600">CBTセッション数</span>
                  <span class="font-semibold">{stats.total_cbt_sessions}</span>
                </div>
                
                <div class="flex justify-between">
                  <span class="text-gray-600">瞑想セッション数</span>
                  <span class="font-semibold">{stats.total_meditation_sessions}</span>
                </div>
                
                <div class="flex justify-between">
                  <span class="text-gray-600">サウンドセッション数</span>
                  <span class="font-semibold">{stats.total_sound_sessions}</span>
                </div>
                
                <div class="flex justify-between">
                  <span class="text-gray-600">ポモドーロセッション数</span>
                  <span class="font-semibold">{stats.total_pomodoro_sessions}</span>
                </div>
                
                {#if stats.average_mood_score !== null}
                  <div class="flex justify-between">
                    <span class="text-gray-600">平均気分スコア</span>
                    <span class="font-semibold">{stats.average_mood_score.toFixed(1)}</span>
                  </div>
                {/if}
                
                {#if stats.last_activity}
                  <div class="flex justify-between">
                    <span class="text-gray-600">最後の活動</span>
                    <span class="font-semibold">{new Date(stats.last_activity).toLocaleDateString('ja-JP')}</span>
                  </div>
                {/if}
              </div>
            {/if}
          </div>
        </div>
      </div>
      
      <!-- アカウント管理 -->
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4">アカウント管理</h2>
        
        <div class="space-y-4">
          <!-- パスワード変更 -->
          <div>
            <button 
              on:click={() => showPasswordForm = !showPasswordForm}
              class="bg-yellow-500 hover:bg-yellow-600 text-white px-4 py-2 rounded shadow"
            >
              {showPasswordForm ? 'キャンセル' : 'パスワードを変更'}
            </button>
            
            {#if showPasswordForm}
              <div class="mt-4 p-4 bg-gray-50 rounded">
                <div class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700">現在のパスワード</label>
                    <input 
                      type="password" 
                      bind:value={passwordForm.current_password}
                      class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700">新しいパスワード</label>
                    <input 
                      type="password" 
                      bind:value={passwordForm.new_password}
                      class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700">新しいパスワード（確認）</label>
                    <input 
                      type="password" 
                      bind:value={passwordForm.confirm_password}
                      class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                </div>
                
                <button 
                  on:click={changePassword}
                  class="mt-4 bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded shadow"
                >
                  パスワードを変更
                </button>
              </div>
            {/if}
          </div>
          
          <!-- アカウント削除 -->
          <div>
            <button 
              on:click={() => showDeleteForm = !showDeleteForm}
              class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded shadow"
            >
              {showDeleteForm ? 'キャンセル' : 'アカウントを削除'}
            </button>
            
            {#if showDeleteForm}
              <div class="mt-4 p-4 bg-red-50 border border-red-200 rounded">
                <p class="text-red-700 mb-4">⚠️ この操作は取り消せません。すべてのデータが削除されます。</p>
                
                <div>
                  <label class="block text-sm font-medium text-red-700">確認用パスワード</label>
                  <input 
                    type="password" 
                    bind:value={deleteForm.password}
                    class="mt-1 block w-full border border-red-300 rounded-md px-3 py-2 focus:outline-none focus:ring-red-500 focus:border-red-500"
                  />
                </div>
                
                <button 
                  on:click={deleteAccount}
                  class="mt-4 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded shadow"
                >
                  アカウントを削除
                </button>
              </div>
            {/if}
          </div>
        </div>
      </div>
    {/if}
  </div>
</main> 