const API_BASE = 'http://localhost:8000/api';

export async function fetchAPI(path: string, options: RequestInit = {}) {
  // localStorageからトークンを取得
  const token = localStorage.getItem('token');
  
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.headers as Record<string, string>
  };

  // トークンがある場合はAuthorizationヘッダーに追加
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers
  });
  
  if (!res.ok) throw new Error(await res.text());
  return res.json();
} 