from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import time as time_type


class WorkingHourBase(BaseModel):
    work_shop_id: Optional[int] = None
    day_of_week: Optional[int] = None
    is_working: Optional[bool] = None
    opening_time: Optional[time_type] = None
    closening_time: Optional[str] = None


class WorkingHourCreate(WorkingHourBase):
    pass


class WorkingHourUpdate(WorkingHourBase):
    pass


class WorkingHourResponse(WorkingHourBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class WorkingHoursListResponse(BaseModel):
    working_hours: List[WorkingHourResponse]