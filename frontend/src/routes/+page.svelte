<script lang="ts">
	import { onMount, onDestroy } from 'svelte';

	// 日時をフォーマットする関数
	function formatDateTime(date: Date): string {
		const year = date.getFullYear();
		const month = String(date.getMonth() + 1).padStart(2, '0');
		const day = String(date.getDate()).padStart(2, '0');
		const hours = String(date.getHours()).padStart(2, '0');
		const minutes = String(date.getMinutes()).padStart(2, '0');
		const seconds = String(date.getSeconds()).padStart(2, '0');
		
		return `${year}年${month}月${day}日 ${hours}:${minutes}:${seconds}`;
	}

	let currentDateTime = formatDateTime(new Date());
	let intervalId: ReturnType<typeof setInterval>;

	// 日時を更新する関数
	function updateDateTime() {
		currentDateTime = formatDateTime(new Date());
	}

	onMount(() => {
		// 初回更新
		updateDateTime();
		
		// 1秒ごとに更新
		intervalId = setInterval(updateDateTime, 1000);
	});

	onDestroy(() => {
		// クリーンアップ
		if (intervalId) {
			clearInterval(intervalId);
		}
	});
</script>

<div class="max-w-4xl mx-auto">
	<div class="text-center">
		<h1 class="text-3xl md:text-4xl font-bold text-gray-800 mb-6 md:mb-8">CareBot AI ホーム</h1>
		
		<!-- 現在時間表示 -->
		<div class="bg-white rounded-lg shadow-lg p-6 md:p-8 mb-6 md:mb-8">
			<h2 class="text-xl md:text-2xl font-semibold text-gray-700 mb-4">現在時刻</h2>
			<div class="text-3xl md:text-5xl lg:text-6xl font-mono text-blue-600 mb-4 break-words">
				{currentDateTime}
			</div>
			<p class="text-gray-500 text-sm md:text-base">リアルタイムで更新されます</p>
		</div>
		
		<!-- ウェルカムメッセージ -->
		<div class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 md:p-6">
			<h3 class="text-lg md:text-xl font-semibold text-gray-800 mb-3">メンタルウェルネスをサポートするAIアシスタント</h3>
			<p class="text-gray-600 text-sm md:text-base leading-relaxed">
				左サイドバーから各機能にアクセスできます。ジャーナル、気分記録、瞑想など、
				あなたのメンタルヘルスをサポートする様々な機能をご利用いただけます。
			</p>
		</div>
	</div>
</div>
