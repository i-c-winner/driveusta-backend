from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.dependencies import get_db
from app.db.repositories.type_work_parents import TypeWorkParentsRepository
from app.schemas.type_work_parents import TypeWorkParentResponse, TypeWorkParentsListResponse

router = APIRouter(
    prefix="/type-work-parents",
    tags=["type_work_parents"]
)

@router.get("/", response_model=TypeWorkParentsListResponse)
async def get_type_work_parents(db: Session = Depends(get_db)):
    """
    Получить список всех типов работ родителей из базы данных
    """
    try:
        type_work_parents_repo = TypeWorkParentsRepository(db)
        type_work_parents = type_work_parents_repo.get_all_type_work_parents()
        
        # Преобразуем модели SQLAlchemy в схемы Pydantic
        type_work_parent_responses = [TypeWorkParentResponse.model_validate(type_work_parent) for type_work_parent in type_work_parents]
        
        return TypeWorkParentsListResponse(type_work_parents=type_work_parent_responses)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@router.get("/{type_work_parent_id}", response_model=TypeWorkParentResponse)
async def get_type_work_parent_by_id(type_work_parent_id: int, db: Session = Depends(get_db)):
    """
    Получить тип работы родителя по ID
    """
    try:
        type_work_parents_repo = TypeWorkParentsRepository(db)
        type_work_parent = type_work_parents_repo.get_type_work_parent_by_id(type_work_parent_id)
        
        if type_work_parent is None:
            raise HTTPException(status_code=404, detail=f"Тип работы родителя с ID {type_work_parent_id} не найден")
        
        type_work_parent_response = TypeWorkParentResponse.model_validate(type_work_parent)
        return type_work_parent_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")