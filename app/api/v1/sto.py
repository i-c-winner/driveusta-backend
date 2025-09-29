from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.dependencies import get_db
from app.db.repositories.sto import StoRepository
from app.schemas.sto import StoResponse, StosListResponse

router = APIRouter(
    prefix="/sto",
    tags=["sto"]
)

@router.get("/by-address/", response_model=StosListResponse)
async def get_stos_by_address(street_name: str, address: str, db: Session = Depends(get_db)):
    """
    Получить СТО по названию улицы и адресу
    """
    try:
        sto_repo = StoRepository(db)
        stos = sto_repo.get_sto_by_address(street_name, address)
        
        # Преобразуем модели SQLAlchemy в схемы Pydantic
        sto_responses = [StoResponse.model_validate(sto) for sto in stos]
        
        return StosListResponse(stos=sto_responses)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@router.get("/", response_model=StosListResponse)
async def get_stos(db: Session = Depends(get_db)):
    """
    Получить список всех СТО из базы данных
    """
    try:
        sto_repo = StoRepository(db)
        stos = sto_repo.get_all_stos()
        
        # Преобразуем модели SQLAlchemy в схемы Pydantic
        sto_responses = [StoResponse.model_validate(sto) for sto in stos]
        
        return StosListResponse(stos=sto_responses)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@router.get("/{sto_id}", response_model=StoResponse)
async def get_sto_by_id(sto_id: int, db: Session = Depends(get_db)):
    """
    Получить СТО по ID
    """
    try:
        sto_repo = StoRepository(db)
        sto = sto_repo.get_sto_by_id(sto_id)
        
        if sto is None:
            raise HTTPException(status_code=404, detail=f"СТО с ID {sto_id} не найдено")
        
        sto_response = StoResponse.model_validate(sto)
        return sto_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")