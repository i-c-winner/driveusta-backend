from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.dependencies import get_db
from app.db.repositories.work_shop import work_shopRepository
from app.schemas.work_shop import work_shopResponse, work_shopsListResponse

router = APIRouter(
    prefix="/work_shop",
    tags=["work_shop"]
)

@router.get("/by-address/", response_model=work_shopsListResponse)
async def get_work_shops_by_address(street_name: str, address: str, db: Session = Depends(get_db)):
    """
    Получить СТО по названию улицы и адресу
    """
    try:
        work_shop_repo = work_shopRepository(db)
        work_shops = work_shop_repo.get_work_shop_by_address(street_name, address)
        
        # Преобразуем модели SQLAlchemy в схемы Pydantic
        work_shop_responses = [work_shopResponse.model_validate(work_shop) for work_shop in work_shops]
        
        return work_shopsListResponse(work_shops=work_shop_responses)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@router.get("/", response_model=work_shopsListResponse)
async def get_work_shops(db: Session = Depends(get_db)):
    """
    Получить список всех СТО из базы данных
    """
    try:
        work_shop_repo = work_shopRepository(db)
        work_shops = work_shop_repo.get_all_work_shops()
        
        # Преобразуем модели SQLAlchemy в схемы Pydantic
        work_shop_responses = [work_shopResponse.model_validate(work_shop) for work_shop in work_shops]
        
        return work_shopsListResponse(work_shops=work_shop_responses)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@router.get("/{work_shop_id}", response_model=work_shopResponse)
async def get_work_shop_by_id(work_shop_id: int, db: Session = Depends(get_db)):
    """
    Получить СТО по ID
    """
    try:
        work_shop_repo = work_shopRepository(db)
        work_shop = work_shop_repo.get_work_shop_by_id(work_shop_id)
        
        if work_shop is None:
            raise HTTPException(status_code=404, detail=f"СТО с ID {work_shop_id} не найдено")
        
        work_shop_response = work_shopResponse.model_validate(work_shop)
        return work_shop_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")