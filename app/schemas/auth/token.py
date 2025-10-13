from typing import Literal
from pydantic import BaseModel

class TokenBase(BaseModel):
   access_token: str
   refresh_token: str
   work_shop_username: str

class CreateToken(TokenBase):
    pass

class RemoveToken(BaseModel):
    work_shop_id: int

class ResponseCreateToken(TokenBase):
    pass

class ResponseRemoveToken(BaseModel):
    work_shop_id: int|bool