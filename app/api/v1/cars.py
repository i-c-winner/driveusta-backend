from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.dependencies import get_db
from app.db.repositories.cars import CarsRepository
from app.schemas.cars import CarResponse, CarsListResponse, CarCreate

router = APIRouter(
    prefix="/cars",
    tags=["cars"]
)

@router.post("/", response_model=CarResponse)
async def create_car(car: CarCreate, db: Session = Depends(get_db)):
    """
    Создать новую машину
    """
    try:
        cars_repo = CarsRepository(db)
        new_car = cars_repo.create_car(car)
        
        car_response = CarResponse.model_validate(new_car)
        return car_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании записи: {str(e)}")

@router.get("/", response_model=CarsListResponse)
async def get_cars(db: Session = Depends(get_db)):
    """
    Получить список всех машин из базы данных
    """
    try:
        cars_repo = CarsRepository(db)
        cars = cars_repo.get_all_cars()
        
        # Преобразуем модели SQLAlchemy в схемы Pydantic
        car_responses = [CarResponse.model_validate(car) for car in cars]
        
        return CarsListResponse(cars=car_responses)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@router.get("/{car_id}", response_model=CarResponse)
async def get_car_by_id(car_id: int, db: Session = Depends(get_db)):
    """
    Получить машину по ID
    """
    try:
        cars_repo = CarsRepository(db)
        car = cars_repo.get_car_by_id(car_id)
        
        if car is None:
            raise HTTPException(status_code=404, detail=f"Машина с ID {car_id} не найдена")
        
        car_response = CarResponse.model_validate(car)
        return car_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")