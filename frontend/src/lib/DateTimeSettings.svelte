<script lang="ts">
	import { datetimeSettings, toggleDateTime, setDateTimePosition } from './stores/datetime.js';
	import type { DateTimePosition } from './stores/datetime.js';

	let isOpen = false;

	function handleToggle() {
		toggleDateTime();
	}

	function handlePositionChange(event: Event) {
		const select = event.target as HTMLSelectElement;
		setDateTimePosition(select.value as DateTimePosition);
	}

	function closeSettings() {
		isOpen = false;
	}
</script>

<div class="datetime-settings">
	<!-- 設定ボタン -->
	<button 
		class="settings-button" 
		on:click={() => isOpen = !isOpen}
		title="日時表示設定"
	>
		<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
			<circle cx="12" cy="12" r="3"/>
			<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
		</svg>
	</button>

	<!-- 設定パネル -->
	{#if isOpen}
		<div class="settings-panel">
			<div class="settings-header">
				<h3>日時表示設定</h3>
				<button class="close-button" on:click={closeSettings}>×</button>
			</div>
			
			<div class="settings-content">
				<div class="setting-item">
					<label>
						<input 
							type="checkbox" 
							checked={$datetimeSettings.show}
							on:change={handleToggle}
						/>
						日時を表示
					</label>
				</div>
				
				<div class="setting-item">
					<label for="position-select">表示位置:</label>
					<select 
						id="position-select"
						value={$datetimeSettings.position}
						on:change={handlePositionChange}
					>
						<option value="top-right">右上</option>
						<option value="top-left">左上</option>
						<option value="bottom-right">右下</option>
						<option value="bottom-left">左下</option>
					</select>
				</div>
				
				<div class="setting-item">
					<small class="format-info">
						表示形式: YYYY/MM/DD HH:mm（1分ごとに更新）
					</small>
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.datetime-settings {
		position: relative;
	}

	.settings-button {
		position: fixed;
		bottom: 20px;
		left: 20px;
		width: 40px;
		height: 40px;
		border-radius: 50%;
		background-color: rgba(0, 0, 0, 0.7);
		color: white;
		border: none;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 999;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
		backdrop-filter: blur(4px);
		transition: all 0.2s ease;
	}

	.settings-button:hover {
		background-color: rgba(0, 0, 0, 0.8);
		transform: scale(1.1);
	}

	.settings-panel {
		position: fixed;
		bottom: 70px;
		left: 20px;
		width: 280px;
		background-color: white;
		border-radius: 8px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
		z-index: 1000;
		overflow: hidden;
	}

	.settings-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 12px 16px;
		background-color: #f8f9fa;
		border-bottom: 1px solid #e9ecef;
	}

	.settings-header h3 {
		margin: 0;
		font-size: 16px;
		font-weight: 600;
		color: #333;
	}

	.close-button {
		background: none;
		border: none;
		font-size: 20px;
		cursor: pointer;
		color: #666;
		padding: 0;
		width: 24px;
		height: 24px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 4px;
	}

	.close-button:hover {
		background-color: #e9ecef;
		color: #333;
	}

	.settings-content {
		padding: 16px;
	}

	.setting-item {
		margin-bottom: 16px;
	}

	.setting-item:last-child {
		margin-bottom: 0;
	}

	.setting-item label {
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 14px;
		color: #333;
		cursor: pointer;
	}

	.setting-item input[type="checkbox"] {
		width: 16px;
		height: 16px;
	}

	.setting-item select {
		width: 100%;
		padding: 8px 12px;
		border: 1px solid #ddd;
		border-radius: 4px;
		font-size: 14px;
		background-color: white;
		margin-top: 4px;
	}

	.setting-item select:focus {
		outline: none;
		border-color: #007bff;
		box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
	}

	.format-info {
		color: #666;
		font-size: 12px;
		margin-top: 8px;
		display: block;
	}

	/* ダークモード対応 */
	@media (prefers-color-scheme: dark) {
		.settings-panel {
			background-color: #2d3748;
			color: #e2e8f0;
		}

		.settings-header {
			background-color: #4a5568;
			border-bottom-color: #718096;
		}

		.settings-header h3 {
			color: #e2e8f0;
		}

			.setting-item label {
		color: #e2e8f0;
	}

	.setting-item select {
		background-color: #4a5568;
		border-color: #718096;
		color: #e2e8f0;
	}

	.format-info {
		color: #a0aec0;
	}
	}

	/* モバイル対応 */
	@media (max-width: 768px) {
		.settings-panel {
			width: calc(100vw - 40px);
			left: 20px;
			right: 20px;
		}

		.settings-button {
			width: 36px;
			height: 36px;
			bottom: 15px;
			left: 15px;
		}

		.settings-panel {
			bottom: 60px;
		}
	}
</style> 