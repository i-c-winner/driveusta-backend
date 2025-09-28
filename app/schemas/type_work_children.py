from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class TypeWorkChildBase(BaseModel):
    type_work_child_name: str
    parent_id: Optional[int] = None


class TypeWorkChildCreate(TypeWorkChildBase):
    pass


class TypeWorkChildResponse(TypeWorkChildBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class TypeWorkChildrenListResponse(BaseModel):
    type_work_children: List[TypeWorkChildResponse]