from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated


from app.db.dependencies import get_db
from app.db.repositories.work_shop import WorkShopRepository
from app.schemas.work_shop import WorkShopResponse, WorkShopsListResponse, WorkShopCreate

router = APIRouter(
    prefix="/work_shop",
    tags=["work_shop"]
)

@router.post("/", response_model=WorkShopResponse)
async def create_work_shop(work_shop: WorkShopCreate, db: Session = Depends(get_db)):
    """
    Создать новое СТО
    """
    try:
        work_shop_repo = WorkShopRepository(db)
        new_work_shop = work_shop_repo.create_work_shop(work_shop)

        work_shop_response = WorkShopResponse.model_validate(new_work_shop)
        return work_shop_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании записи: {str(e)}")


@router.get("/by-address/", response_model=WorkShopsListResponse)
async def get_work_shops_by_address(street_name: str, address: str, db: Session = Depends(get_db)):
    """
    Получить СТО по названию улицы и адресу
    """
    try:
        work_shop_repo = WorkShopRepository(db)
        work_shops = work_shop_repo.get_work_shop_by_address(street_name, address)
        
        # Преобразуем модели SQLAlchemy в схемы Pydantic
        work_shop_responses = [WorkShopResponse.model_validate(work_shop) for work_shop in work_shops]
        
        return WorkShopsListResponse(work_shops=work_shop_responses)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@router.get("/", response_model=WorkShopsListResponse)
async def get_work_shops(db: Session = Depends(get_db)):
    """
    Получить список всех СТО из базы данных
    """
    try:
        work_shop_repo = WorkShopRepository(db)
        work_shops = work_shop_repo.get_all_work_shops()
        
        # Преобразуем модели SQLAlchemy в схемы Pydantic
        work_shop_responses = [WorkShopResponse.model_validate(work_shop) for work_shop in work_shops]
        
        return WorkShopsListResponse(work_shops=work_shop_responses)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")


@router.get("/{work-shop-id}", response_model=WorkShopResponse)
async def get_work_shop_by_id(work_shop_id: int, db: Session = Depends(get_db)):
    """
    Получить СТО по ID
    """
    try:
        work_shop_repo = WorkShopRepository(db)
        work_shop = work_shop_repo.get_work_shop_by_id(work_shop_id)

        if work_shop is None:
            raise HTTPException(status_code=404, detail=f"СТО с ID {work_shop_id} не найдено")

        work_shop_response = WorkShopResponse.model_validate(work_shop)
        return work_shop_response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

