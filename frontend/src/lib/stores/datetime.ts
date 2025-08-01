import { writable } from 'svelte/store';

export type DateTimePosition = 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left';

interface DateTimeSettings {
	show: boolean;
	position: DateTimePosition;
	format: string;
}

// デフォルト設定
const defaultSettings: DateTimeSettings = {
	show: true,
	position: 'top-right',
	format: 'YYYY/MM/DD HH:mm'
};

// ローカルストレージから設定を読み込み
function loadSettings(): DateTimeSettings {
	if (typeof window !== 'undefined') {
		const saved = localStorage.getItem('datetime-settings');
		if (saved) {
			try {
				return { ...defaultSettings, ...JSON.parse(saved) };
			} catch (e) {
				console.warn('Failed to load datetime settings:', e);
			}
		}
	}
	return defaultSettings;
}

// ストアの作成
export const datetimeSettings = writable<DateTimeSettings>(loadSettings());

// 設定を保存する関数
export function saveDateTimeSettings(settings: Partial<DateTimeSettings>) {
	datetimeSettings.update(current => {
		const newSettings = { ...current, ...settings };
		
		// ローカルストレージに保存
		if (typeof window !== 'undefined') {
			localStorage.setItem('datetime-settings', JSON.stringify(newSettings));
		}
		
		return newSettings;
	});
}

// 表示/非表示を切り替える関数
export function toggleDateTime() {
	datetimeSettings.update(settings => ({
		...settings,
		show: !settings.show
	}));
}

// 位置を変更する関数
export function setDateTimePosition(position: DateTimePosition) {
	datetimeSettings.update(settings => ({
		...settings,
		position
	}));
} 