from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class work_shopBase(BaseModel):
    work_shop_name: Optional[str] = None
    telephone: Optional[str] = None
    street_name: Optional[str] = None
    address: Optional[str] = None
    site: Optional[str] = None
    rating: Optional[float] = None


class work_shopCreate(work_shopBase):
    pass


class work_shopResponse(work_shopBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class work_shopsListResponse(BaseModel):
    work_shops: List[work_shopResponse]