from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class WorkShopBase(BaseModel):
    work_shop_name: Optional[str] = None
    telephone: Optional[str] = None
    street_name: Optional[str] = None
    address: Optional[str] = None
    site: Optional[str] = None
    rating: Optional[float] = None


class WorkShopCreate(WorkShopBase):
    pass


class WorkShopResponse(WorkShopBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class WorkShopsListResponse(BaseModel):
    work_shops: List[WorkShopResponse]