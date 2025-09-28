from pydantic import BaseModel, ConfigDict
from typing import List


class CarBase(BaseModel):
    brand: str


class CarCreate(CarBase):
    pass


class CarResponse(BaseModel):
    id: int
    car_name: str
    
    model_config = ConfigDict(from_attributes=True)


class CarsListResponse(BaseModel):
    cars: List[CarResponse]

