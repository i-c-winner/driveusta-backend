from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class AvailableCarBase(BaseModel):
    car_name: Optional[str] = None
    work_shop_id: Optional[int] = None
    cars_id: Optional[int] = None


class AvailableCarCreate(AvailableCarBase):
    pass


class AvailableCarResponse(AvailableCarBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class AvailableCarsListResponse(BaseModel):
    available_cars: List[AvailableCarResponse]