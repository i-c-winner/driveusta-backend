from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class AddressBase(BaseModel):
    number: Optional[str] = None
    id_work_shop: Optional[int] = None


class AddressCreate(AddressBase):
    pass


class AddressResponse(AddressBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class AddressesListResponse(BaseModel):
    addresses: List[AddressResponse]