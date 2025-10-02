from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class HolidayBase(BaseModel):
    work_shop_id: int
    description: Optional[str] = None


class HolidayCreate(HolidayBase):
    pass


class HolidayUpdate(BaseModel):
    work_shop_id: Optional[int] = None
    description: Optional[str] = None


class HolidayResponse(HolidayBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class HolidaysListResponse(BaseModel):
    holidays: List[HolidayResponse]