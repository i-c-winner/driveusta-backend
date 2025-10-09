# security.py
import os

from argon2 import PasswordHasher
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from pydantic import BaseModel

from app.models import WorkShop

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key_for_development")

# Секретный ключ для подписи токена. Должен быть строго секретным!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class TokenData(BaseModel):
    username: str = None

password_hash= PasswordHash.recommended()

def verify_password(plan_password, hash_password):
    return password_hash.verify(plan_password, hash_password)

def get_password_hash(password):
    return password_hash.hash(password)

def authenticate_work_shop(db, login: str, password: str):
    work_shop = db.query(WorkShop).filter(WorkShop.work_shop_login == login).first()
    if not work_shop:
        return False
    if not verify_password(password, work_shop.hash_password):
        return False
    return work_shop

def create_tokens(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """Проверяет токен и возвращает данные из него. Если токен невалиден - вернет None"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None