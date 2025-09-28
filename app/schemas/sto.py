from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class StoBase(BaseModel):
    sto_name: Optional[str] = None
    telephone: Optional[str] = None
    street_name: Optional[str] = None
    address: Optional[str] = None
    site: Optional[str] = None
    rating: Optional[float] = None


class StoCreate(StoBase):
    pass


class StoResponse(StoBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class StosListResponse(BaseModel):
    stos: List[StoResponse]