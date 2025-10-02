from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date, time, datetime


class AppointmentBase(BaseModel):
    client_name: Optional[str] = None
    client_phone: Optional[str] = None
    car_license_plate: Optional[str] = None
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    duration_minutes: Optional[int] = None
    time: Optional[datetime] = None
    description: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(AppointmentBase):
    pass


class AppointmentResponse(AppointmentBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class AppointmentsListResponse(BaseModel):
    appointments: List[AppointmentResponse]