import os
from datetime import datetime, timedelta

from fastapi import HTTPException
from fastapi.params import Depends
from jose import jwt, JWTError
from dotenv import load_dotenv
from passlib.hash import bcrypt
from fastapi.security import OAuth2PasswordBearer

load_dotenv()
SECRET_KEY_ACCESS = os.getenv("SECRET_KEY_ACCESS")
if SECRET_KEY_ACCESS is None:
    raise ValueError("SECRET_KEY_ACCESS not set. Please set SECRET_KEY_ACCESS environment variable for PostgreSQL connection.")
SECRET_KEY_REFRESH = os.getenv("SECRET_KEY_REFRESH")
if SECRET_KEY_REFRESH is None:
    raise ValueError("SECRET_KEY_REFRESH not set. Please set SECRET_KEY_REFRESH environment variable for PostgreSQL connection.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300000

ouath2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/register")
def create_tokens(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt_access = jwt.encode(to_encode, SECRET_KEY_ACCESS, algorithm=ALGORITHM)
    encoded_jwt_refresh = jwt.encode(to_encode, SECRET_KEY_REFRESH, algorithm=ALGORITHM)

    return {
     "access_token":   encoded_jwt_access,
     "refresh_token":  encoded_jwt_refresh,
     "work_shop_username": data["work_shop_username"]
    }
def create_hash_password(password: str):
    print(">>> type:", type(password), "value:", password)
    return bcrypt.hash(password)
    # return 'sss'

def get_current_username(token = Depends(ouath2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY_ACCESS or "", algorithms=[ALGORITHM])
        username = payload.get("work_shop_username")
        print(username)
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token JWT")