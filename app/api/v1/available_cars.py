from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.dependencies import get_db
from app.db.repositories.available_cars import AvailableCarsRepository
from app.schemas.available_cars import AvailableCarResponse, AvailableCarsListResponse, AvailableCarCreate

router = APIRouter(
    prefix="/available-cars",
    tags=["available_cars"]
)

@router.post("/", response_model=AvailableCarResponse)
async def create_available_car(available_car: AvailableCarCreate, db: Session = Depends(get_db)):
    """
    Создать новый доступный автомобиль
    """
    try:
        available_cars_repo = AvailableCarsRepository(db)
        new_available_car = available_cars_repo.create_available_car(available_car)
        
        available_car_response = AvailableCarResponse.model_validate(new_available_car)
        return available_car_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании записи: {str(e)}")

@router.get("/", response_model=AvailableCarsListResponse)
async def get_available_cars(db: Session = Depends(get_db)):
    """
    Получить список всех доступных автомобилей из базы данных
    """
    try:
        available_cars_repo = AvailableCarsRepository(db)
        available_cars = available_cars_repo.get_all_available_cars()
        
        # Преобразуем модели SQLAlchemy в схемы Pydantic
        available_car_responses = [AvailableCarResponse.model_validate(available_car) for available_car in available_cars]
        
        return AvailableCarsListResponse(available_cars=available_car_responses)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@router.get("/{available_car_id}", response_model=AvailableCarResponse)
async def get_available_car_by_id(available_car_id: int, db: Session = Depends(get_db)):
    """
    Получить доступный автомобиль по ID
    """
    try:
        available_cars_repo = AvailableCarsRepository(db)
        available_car = available_cars_repo.get_available_car_by_id(available_car_id)
        
        if available_car is None:
            raise HTTPException(status_code=404, detail=f"Доступный автомобиль с ID {available_car_id} не найден")
        
        available_car_response = AvailableCarResponse.model_validate(available_car)
        return available_car_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")