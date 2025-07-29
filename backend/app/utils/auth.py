import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
import bcrypt
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# JWT設定（環境変数から取得）
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# 本番環境では必ず環境変数から取得するように警告
if os.getenv("ENVIRONMENT") == "production":
    if not os.getenv("JWT_SECRET_KEY"):
        raise ValueError("本番環境ではJWT_SECRET_KEYの環境変数が必須です")

security = HTTPBearer()

def hash_password(password: str) -> str:
    """パスワードをハッシュ化"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """パスワードを検証"""
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: timedelta = None):
    """アクセストークンを作成"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """トークンを検証"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            print(f"トークンにsubフィールドがありません: {payload}")
            return None
        print(f"トークン検証成功: user_id = {user_id}")
        return user_id
    except JWTError as e:
        print(f"JWT検証エラー: {e}")
        return None
    except Exception as e:
        print(f"トークン検証エラー: {e}")
        return None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """現在のユーザーを取得"""
    token = credentials.credentials
    print(f"トークン受信: {token[:50]}...")
    
    user_id = verify_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"ユーザーID取得: {user_id}")
    
    # 循環インポートを避けるため、ここでSupabaseDBをインポート
    from app.database.supabase_db import SupabaseDB
    user = SupabaseDB.get_user_by_id(int(user_id))
    if user is None:
        print(f"ユーザーが見つかりません: ID {user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"ユーザー取得成功: {user}")
    return user

def get_current_user_optional(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """現在のユーザーを取得（オプショナル）"""
    try:
        return get_current_user(credentials)
    except HTTPException:
        return None 