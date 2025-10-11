import os
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY_ACCESS = os.getenv("SECRET_KEY_ACCESS")
if SECRET_KEY_ACCESS is None:
    raise ValueError("SECRET_KEY_ACCESS not set. Please set SECRET_KEY_ACCESS environment variable for PostgreSQL connection.")
SECRET_KEY_REFRESH = os.getenv("SECRET_KEY_REFRESH")
if SECRET_KEY_REFRESH is None:
    raise ValueError("SECRET_KEY_REFRESH not set. Please set SECRET_KEY_REFRESH environment variable for PostgreSQL connection.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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




