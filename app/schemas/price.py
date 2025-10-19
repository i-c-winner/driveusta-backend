from pydantic import BaseModel
from typing import Optional


class PriceCreate(BaseModel):
    work_type_children_id: int
    price: float


class PriceResponse(BaseModel):
    work_type_children_id: int
    price: float

    class Config:
        from_attributes = True