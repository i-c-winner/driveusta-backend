from pydantic import BaseModel, ConfigDict
from typing import List


class TypeWorkParentBase(BaseModel):
    type_work_parent_name: str


class TypeWorkParentCreate(TypeWorkParentBase):
    pass


class TypeWorkParentResponse(TypeWorkParentBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class TypeWorkParentsListResponse(BaseModel):
    type_work_parents: List[TypeWorkParentResponse]