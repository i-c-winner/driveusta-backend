from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class HolidayBase(BaseModel):
    description: Optional[str] = None


class HolidayCreate(HolidayBase):
    pass


class HolidayUpdate(HolidayBase):
    pass


class HolidayResponse(HolidayBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class HolidaysListResponse(BaseModel):
    holidays: List[HolidayResponse]