from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class WorkShopBase(BaseModel):
    work_shop_name: str = ''
    telephone: str = ''
    street_name: str = ''
    address: str = ''
    site: str = ''
    rating: float = 0.0
    hash_password: str = ''
    login: str = ''


class WorkShopCreate(WorkShopBase):
    pass


class WorkShopResponse(WorkShopBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class WorkShopsListResponse(BaseModel):
    work_shops: List[WorkShopResponse]
