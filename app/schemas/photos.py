from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class PhotoBase(BaseModel):
    url: Optional[str] = None
    id_sto: Optional[int] = None


class PhotoCreate(PhotoBase):
    pass


class PhotoResponse(PhotoBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class PhotosListResponse(BaseModel):
    photos: List[PhotoResponse]