from pydantic import BaseModel

class Register(BaseModel):
    username: str
    password: str

class RegisterResponse(BaseModel):
    work_shop_id: int
    access_token: str
    refresh_token: str
