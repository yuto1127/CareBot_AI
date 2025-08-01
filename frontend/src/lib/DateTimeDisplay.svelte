<script lang="ts">
	import { onMount, onDestroy } from 'svelte';

	// Props（オプション）
	let { show = true, position = 'top-right' } = $props<{
		show?: boolean;
		position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left';
	}>();

	// 日時をフォーマットする関数
	function formatDateTime(date: Date): string {
		const year = date.getFullYear();
		const month = String(date.getMonth() + 1).padStart(2, '0');
		const day = String(date.getDate()).padStart(2, '0');
		const hours = String(date.getHours()).padStart(2, '0');
		const minutes = String(date.getMinutes()).padStart(2, '0');
		
		return `${year}/${month}/${day} ${hours}:${minutes}`;
	}

	let currentDateTime = formatDateTime(new Date()); // 初期値を設定
	let intervalId: ReturnType<typeof setInterval>;

	// 日時を更新する関数
	function updateDateTime() {
		currentDateTime = formatDateTime(new Date());
	}

	onMount(() => {
		// 初回更新
		updateDateTime();
		
		// 1分ごとに更新
		intervalId = setInterval(updateDateTime, 60000);
	});

	onDestroy(() => {
		// クリーンアップ
		if (intervalId) {
			clearInterval(intervalId);
		}
	});
</script>

{#if show}
	<div class="datetime-display" class:top-right={position === 'top-right'} class:top-left={position === 'top-left'} class:bottom-right={position === 'bottom-right'} class:bottom-left={position === 'bottom-left'}>
		{currentDateTime}
	</div>
{/if}

<style>
	.datetime-display {
		position: fixed;
		background-color: rgba(0, 0, 0, 0.8);
		color: white;
		padding: 8px 12px;
		border-radius: 6px;
		font-family: 'Courier New', monospace;
		font-size: 14px;
		font-weight: 500;
		z-index: 1000;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
		backdrop-filter: blur(4px);
	}

	.datetime-display.top-right {
		top: 10px;
		right: 10px;
	}

	.datetime-display.top-left {
		top: 10px;
		left: 10px;
	}

	.datetime-display.bottom-right {
		bottom: 10px;
		right: 10px;
	}

	.datetime-display.bottom-left {
		bottom: 10px;
		left: 10px;
	}

	/* ダークモード対応 */
	@media (prefers-color-scheme: dark) {
		.datetime-display {
			background-color: rgba(255, 255, 255, 0.1);
			color: #e5e5e5;
		}
	}

	/* モバイル対応 */
	@media (max-width: 768px) {
		.datetime-display {
			font-size: 12px;
			padding: 6px 10px;
		}
		
		.datetime-display.top-right {
			top: 5px;
			right: 5px;
		}
		
		.datetime-display.top-left {
			top: 5px;
			left: 5px;
		}
		
		.datetime-display.bottom-right {
			bottom: 5px;
			right: 5px;
		}
		
		.datetime-display.bottom-left {
			bottom: 5px;
			left: 5px;
		}
	}
</style> 