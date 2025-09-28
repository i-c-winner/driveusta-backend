from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.dependencies import get_db
from app.db.repositories.type_work_children import TypeWorkChildrenRepository
from app.schemas.type_work_children import TypeWorkChildResponse, TypeWorkChildrenListResponse

router = APIRouter(
    prefix="/type-work-children",
    tags=["type_work_children"]
)

@router.get("/", response_model=TypeWorkChildrenListResponse)
async def get_type_work_children(db: Session = Depends(get_db)):
    """
    Получить список всех типов работ детей из базы данных
    """
    try:
        type_work_children_repo = TypeWorkChildrenRepository(db)
        type_work_children = type_work_children_repo.get_all_type_work_children()
        
        # Преобразуем модели SQLAlchemy в схемы Pydantic
        type_work_child_responses = [TypeWorkChildResponse.model_validate(type_work_child) for type_work_child in type_work_children]
        
        return TypeWorkChildrenListResponse(type_work_children=type_work_child_responses)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@router.get("/{type_work_child_id}", response_model=TypeWorkChildResponse)
async def get_type_work_child_by_id(type_work_child_id: int, db: Session = Depends(get_db)):
    """
    Получить тип работы ребенка по ID
    """
    try:
        type_work_children_repo = TypeWorkChildrenRepository(db)
        type_work_child = type_work_children_repo.get_type_work_child_by_id(type_work_child_id)
        
        if type_work_child is None:
            raise HTTPException(status_code=404, detail=f"Тип работы ребенка с ID {type_work_child_id} не найден")
        
        type_work_child_response = TypeWorkChildResponse.model_validate(type_work_child)
        return type_work_child_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")