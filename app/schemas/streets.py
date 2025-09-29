from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class StreetBase(BaseModel):
    street_name: Optional[str] = None
    id_sto: Optional[int] = None


class StreetCreate(StreetBase):
    pass


class StreetResponse(StreetBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)



class StreetsListResponse(BaseModel):
    streets: List[StreetResponse]