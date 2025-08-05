<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { authStore } from '$lib/stores/auth';

	let { children } = $props();
	
	let isLoggedIn = false;
	let user: any = null;
	let isSidebarOpen = false;
	
	// ストアから認証状態を購読
	authStore.subscribe((auth) => {
		isLoggedIn = auth.isLoggedIn;
		user = auth.user;
		console.log('認証状態更新:', { isLoggedIn, user });
	});
	
	// デバッグ用：現在のlocalStorageの状態を確認
	onMount(() => {
		if (typeof window !== 'undefined') {
			const userData = localStorage.getItem('user');
			console.log('localStorage確認:', { userData });
		}
	});
	
	onMount(() => {
		// 初期状態をチェック
		authStore.checkLoginStatus();
	});
	
	function logout() {
		authStore.logout();
	}
	
	function toggleSidebar() {
		isSidebarOpen = !isSidebarOpen;
		console.log('サイドバー切り替え:', isSidebarOpen);
	}
</script>

<div class="min-h-screen bg-gray-50">
	<!-- ヘッダー -->
	<header class="bg-white shadow-sm border-b border-gray-200">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
			<div class="flex justify-between items-center h-16">
				<!-- ハンバーガーメニュー（モバイル） -->
				<div class="md:hidden">
					<button 
						on:click={toggleSidebar}
						class="text-gray-600 hover:text-gray-800 focus:outline-none p-2"
						title="メニューを開く"
					>
						<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
						</svg>
					</button>
				</div>
				
				<!-- タイトル -->
				<div class="flex items-center">
					<h1 class="text-xl font-bold text-blue-600">CareBot AI</h1>
				</div>
				
				<!-- アカウント関連ボタン -->
				<div class="flex items-center space-x-4">
					<a href="/login" class="text-sm text-blue-600 hover:text-blue-800">ログイン</a>
					<a href="/register" class="text-sm text-green-600 hover:text-green-800">新規登録</a>
				</div>
			</div>
		</div>
	</header>

	<div class="flex">
		<!-- サイドバー（デスクトップ） -->
		<aside class="hidden md:block w-64 bg-white shadow-sm min-h-screen">
			<nav class="mt-8">
				<div class="px-4 space-y-2">
					<a href="/" class="flex items-center px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-700 rounded-md {$page.url.pathname === '/' ? 'bg-blue-100 text-blue-700' : ''}">
						<span class="text-lg mr-3">🏠</span>
						ホーム
					</a>
					
					{#if isLoggedIn}
						<a href="/dashboard" class="flex items-center px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-700 rounded-md {$page.url.pathname === '/dashboard' ? 'bg-blue-100 text-blue-700' : ''}">
							<span class="text-lg mr-3">📊</span>
							ダッシュボード
						</a>
					{/if}
					
					<a href="/journals" class="flex items-center px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-700 rounded-md {$page.url.pathname === '/journals' ? 'bg-blue-100 text-blue-700' : ''}">
						<span class="text-lg mr-3">📝</span>
						ジャーナル
					</a>
					
					<a href="/moods" class="flex items-center px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-700 rounded-md {$page.url.pathname === '/moods' ? 'bg-blue-100 text-blue-700' : ''}">
						<span class="text-lg mr-3">😊</span>
						気分記録
					</a>
					
					{#if isLoggedIn}
						<a href="/cbt" class="flex items-center px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-700 rounded-md {$page.url.pathname === '/cbt' ? 'bg-blue-100 text-blue-700' : ''}">
							<span class="text-lg mr-3">🧠</span>
							CBTセッション
						</a>
						
						<a href="/analysis" class="flex items-center px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-700 rounded-md {$page.url.pathname === '/analysis' ? 'bg-blue-100 text-blue-700' : ''}">
							<span class="text-lg mr-3">🤖</span>
							AI分析
						</a>
					{/if}
					
					<a href="/meditation" class="flex items-center px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-700 rounded-md {$page.url.pathname === '/meditation' ? 'bg-blue-100 text-blue-700' : ''}">
						<span class="text-lg mr-3">🧘‍♀️</span>
						瞑想
					</a>
					
					<a href="/sounds" class="flex items-center px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-700 rounded-md {$page.url.pathname === '/sounds' ? 'bg-blue-100 text-blue-700' : ''}">
						<span class="text-lg mr-3">🎵</span>
						リラックスサウンド
					</a>
					
					<a href="/pomodoro" class="flex items-center px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-700 rounded-md {$page.url.pathname === '/pomodoro' ? 'bg-blue-100 text-blue-700' : ''}">
						<span class="text-lg mr-3">⏰</span>
						ポモドーロタイマー
					</a>
				</div>
			</nav>
		</aside>

		<!-- モバイルサイドバー（オーバーレイ） -->
		<!-- デバッグ: isSidebarOpen = {isSidebarOpen} -->
		{#if isSidebarOpen}
			<!-- オーバーレイ -->
			<div class="fixed inset-0 z-50 bg-black bg-opacity-50 md:hidden" on:click={toggleSidebar}></div>
			
			<!-- サイドバー -->
			<div class="fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-2xl md:hidden">
				<!-- ヘッダー -->
				<div class="flex items-center justify-between h-16 px-4 border-b border-gray-200 bg-white">
					<h2 class="text-lg font-semibold text-gray-800">メニュー</h2>
					<button 
						on:click={toggleSidebar}
						class="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded"
					>
						<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
						</svg>
					</button>
				</div>
				
				<!-- ナビゲーション -->
				<nav class="flex-1 px-4 py-6 space-y-2 bg-white overflow-y-auto">
					<a href="/" class="flex items-center px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-700 rounded-md transition-colors" on:click={toggleSidebar}>
						<span class="text-xl mr-3">🏠</span>
						<span class="font-medium">ホーム</span>
					</a>
					
					<a href="/dashboard" class="flex items-center px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-700 rounded-md transition-colors" on:click={toggleSidebar}>
						<span class="text-xl mr-3">📊</span>
						<span class="font-medium">ダッシュボード</span>
					</a>
					
					<a href="/journals" class="flex items-center px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-700 rounded-md transition-colors" on:click={toggleSidebar}>
						<span class="text-xl mr-3">📝</span>
						<span class="font-medium">ジャーナル</span>
					</a>
					
					<a href="/moods" class="flex items-center px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-700 rounded-md transition-colors" on:click={toggleSidebar}>
						<span class="text-xl mr-3">😊</span>
						<span class="font-medium">気分記録</span>
					</a>
					
					<a href="/cbt" class="flex items-center px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-700 rounded-md transition-colors" on:click={toggleSidebar}>
						<span class="text-xl mr-3">🧠</span>
						<span class="font-medium">CBTセッション</span>
					</a>
					
					<a href="/analysis" class="flex items-center px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-700 rounded-md transition-colors" on:click={toggleSidebar}>
						<span class="text-xl mr-3">🤖</span>
						<span class="font-medium">AI分析</span>
					</a>
					
					<a href="/meditation" class="flex items-center px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-700 rounded-md transition-colors" on:click={toggleSidebar}>
						<span class="text-xl mr-3">🧘‍♀️</span>
						<span class="font-medium">瞑想</span>
					</a>
					
					<a href="/sounds" class="flex items-center px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-700 rounded-md transition-colors" on:click={toggleSidebar}>
						<span class="text-xl mr-3">🎵</span>
						<span class="font-medium">リラックスサウンド</span>
					</a>
					
					<a href="/pomodoro" class="flex items-center px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-700 rounded-md transition-colors" on:click={toggleSidebar}>
						<span class="text-xl mr-3">⏰</span>
						<span class="font-medium">ポモドーロタイマー</span>
					</a>
				</nav>
			</div>
		{/if}

		<!-- メインコンテンツ -->
		<main class="flex-1 p-4 lg:p-8">
			{@render children()}
		</main>
	</div>
</div>
