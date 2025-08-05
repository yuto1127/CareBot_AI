import { writable } from 'svelte/store';

interface User {
	username?: string;
	email?: string;
	id?: number;
	[key: string]: any;
}

interface AuthState {
	isLoggedIn: boolean;
	user: User | null;
}

function createAuthStore() {
	const { subscribe, set, update } = writable<AuthState>({
		isLoggedIn: false,
		user: null
	});

	// ログイン状態をチェックする関数
	function checkLoginStatus() {
		// ブラウザ環境でのみlocalStorageにアクセス
		if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
			const userData = localStorage.getItem('user');
			if (userData) {
				try {
					const user = JSON.parse(userData);
					set({ isLoggedIn: true, user });
					console.log('ログイン済み:', user);
				} catch (e) {
					console.error('ユーザーデータの解析エラー:', e);
					localStorage.removeItem('user');
					set({ isLoggedIn: false, user: null });
				}
			} else {
				set({ isLoggedIn: false, user: null });
				console.log('未ログイン');
			}
		}
	}

	// ログイン関数
	function login(userData: User) {
		if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
			localStorage.setItem('user', JSON.stringify(userData));
		}
		set({ isLoggedIn: true, user: userData });
	}

	// ログアウト関数
	function logout() {
		if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
			localStorage.removeItem('user');
			localStorage.removeItem('token');
		}
		set({ isLoggedIn: false, user: null });
	}

	return {
		subscribe,
		login,
		logout,
		checkLoginStatus
	};
}

export const authStore = createAuthStore(); 