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

  const url = `${API_BASE}${path}`;
  const method = options.method || 'GET';
  
  // リクエストログ
  console.log(`🌐 API Request: ${method} ${url}`);
  if (options.body) {
    try {
      const bodyData = JSON.parse(options.body as string);
      // パスワードをマスクしてログ出力
      const maskedBody = { ...bodyData };
      if (maskedBody.password) {
        maskedBody.password = '***';
      }
      console.log('📤 Request Body:', maskedBody);
    } catch (e) {
      console.log('📤 Request Body: [JSON parse error]');
    }
  }

  const res = await fetch(url, {
    ...options,
    headers
  });
  
  // レスポンスログ
  console.log(`📥 API Response: ${method} ${url} - Status: ${res.status}`);
  
  if (!res.ok) {
    const errorText = await res.text();
    console.error(`❌ API Error: ${method} ${url} - ${res.status}: ${errorText}`);
    throw new Error(errorText);
  }
  
  const responseData = await res.json();
  console.log(`✅ API Success: ${method} ${url}`, responseData);
  
  return responseData;
} 