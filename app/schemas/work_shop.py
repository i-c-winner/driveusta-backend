from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class WorkShopBase(BaseModel):
    work_shop_name: str = None
    telephone: str = None
    street_name: str = None
    address: str = None
    site: str = None
    rating: float = None


class WorkShopCreate(WorkShopBase):
    pass


class WorkShopResponse(WorkShopBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class WorkShopsListResponse(BaseModel):
    work_shops: List[WorkShopResponse]