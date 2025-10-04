from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class ParticipantBase(BaseModel):
    password: str = None
    email: str = None
    login: Optional[str] = None
    vin: Optional[float] = None
    car_id: Optional[int] = None



class ParticipantCreate(ParticipantBase):
    pass


class ParticipantResponse(ParticipantBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class ParticipantsListResponse(BaseModel):
    participants: List[ParticipantResponse]