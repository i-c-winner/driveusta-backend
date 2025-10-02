from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.dependencies import get_db
from app.db.repositories.calendar.holidays import HolidayRepository
from app.schemas.calendar.holidays import HolidayResponse, HolidaysListResponse, HolidayCreate, HolidayUpdate

router = APIRouter(
    prefix="/calendar/holidays",
    tags=["calendar", "holidays"]
)

@router.post("/", response_model=HolidayResponse)
async def create_holiday(holiday: HolidayCreate, db: Session = Depends(get_db)):
    """
    Создать новый праздник
    """
    try:
        holiday_repo = HolidayRepository(db)
        new_holiday = holiday_repo.create_holiday(holiday)
        
        holiday_response = HolidayResponse.model_validate(new_holiday)
        return holiday_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании записи: {str(e)}")

@router.get("/", response_model=HolidaysListResponse)
async def get_holidays(db: Session = Depends(get_db)):
    """
    Получить список всех праздников из базы данных
    """
    try:
        holiday_repo = HolidayRepository(db)
        holidays = holiday_repo.get_all_holidays()
        
        # Преобразуем модели SQLAlchemy в схемы Pydantic
        holiday_responses = [HolidayResponse.model_validate(holiday) for holiday in holidays]
        
        return HolidaysListResponse(holidays=holiday_responses)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@router.get("/{holiday_id}", response_model=HolidayResponse)
async def get_holiday_by_id(holiday_id: int, db: Session = Depends(get_db)):
    """
    Получить праздник по ID
    """
    try:
        holiday_repo = HolidayRepository(db)
        holiday = holiday_repo.get_holiday_by_id(holiday_id)
        
        if holiday is None:
            raise HTTPException(status_code=404, detail=f"Праздник с ID {holiday_id} не найден")
        
        holiday_response = HolidayResponse.model_validate(holiday)
        return holiday_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@router.put("/{holiday_id}", response_model=HolidayResponse)
async def update_holiday(holiday_id: int, holiday: HolidayUpdate, db: Session = Depends(get_db)):
    """
    Обновить праздник по ID
    """
    try:
        holiday_repo = HolidayRepository(db)
        updated_holiday = holiday_repo.update_holiday(holiday_id, holiday)
        
        if updated_holiday is None:
            raise HTTPException(status_code=404, detail=f"Праздник с ID {holiday_id} не найден")
        
        holiday_response = HolidayResponse.model_validate(updated_holiday)
        return holiday_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении данных: {str(e)}")

@router.delete("/{holiday_id}")
async def delete_holiday(holiday_id: int, db: Session = Depends(get_db)):
    """
    Удалить праздник по ID
    """
    try:
        holiday_repo = HolidayRepository(db)
        result = holiday_repo.delete_holiday(holiday_id)
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Праздник с ID {holiday_id} не найден")
        
        return {"message": f"Праздник с ID {holiday_id} успешно удален"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении данных: {str(e)}")