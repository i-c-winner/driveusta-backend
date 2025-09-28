from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.dependencies import get_db
from app.db.repositories.streets import StreetsRepository
from app.schemas.streets import StreetResponse, StreetsListResponse

router = APIRouter(
    prefix="/streets",
    tags=["streets"]
)

@router.get("/", response_model=StreetsListResponse)
async def get_streets(db: Session = Depends(get_db)):
    """
    Получить список всех улиц из базы данных
    """
    try:
        streets_repo = StreetsRepository(db)
        streets = streets_repo.get_all_streets()
        
        # Преобразуем модели SQLAlchemy в схемы Pydantic
        street_responses = [StreetResponse.model_validate(street) for street in streets]
        
        return StreetsListResponse(streets=street_responses)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@router.get("/{street_id}", response_model=StreetResponse)
async def get_street_by_id(street_id: int, db: Session = Depends(get_db)):
    """
    Получить улицу по ID
    """
    try:
        streets_repo = StreetsRepository(db)
        street = streets_repo.get_street_by_id(street_id)
        
        if street is None:
            raise HTTPException(status_code=404, detail=f"Улица с ID {street_id} не найдена")
        
        street_response = StreetResponse.model_validate(street)
        return street_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")