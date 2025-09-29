from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class CarBase(BaseModel):
    car_name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None


class CarCreate(CarBase):
    pass


class CarResponse(CarBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class CarsListResponse(BaseModel):
    cars: List[CarResponse]