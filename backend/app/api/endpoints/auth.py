from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.user import User
from app.utils.auth import create_access_token, verify_token
from app.database.supabase_db import SupabaseDB
from app.schemas.user import UserCreate, UserLogin, Token
from passlib.context import CryptContext
from datetime import timedelta

router = APIRouter()

# パスワードハッシュ化
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(email: str, password: str):
    user = SupabaseDB.get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user['password']):
        return False
    return user

@router.post("/register", response_model=Token)
def register(user_data: UserCreate):
    # 既存ユーザーチェック
    existing_user = SupabaseDB.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # パスワードハッシュ化
    hashed_password = get_password_hash(user_data.password)
    
    # 新規ユーザー作成
    user_create_data = UserCreate(
        email=user_data.email,
        password=hashed_password,
        name=user_data.name
    )
    
    db_user = SupabaseDB.create_user(user_create_data)
    if not db_user:
        raise HTTPException(
            status_code=500,
            detail="Failed to create user"
        )
    
    # トークン作成
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(db_user['id'])}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user['id'],
            "email": db_user['email'],
            "name": db_user['name'],
            "plan_type": db_user.get('plan_type', 'free')
        }
    }

@router.post("/login", response_model=Token)
def login(user_data: UserLogin):
    user = authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user['id'])}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user['id'],
            "email": user['email'],
            "name": user['name'],
            "plan_type": user.get('plan_type', 'free')
        }
    } 