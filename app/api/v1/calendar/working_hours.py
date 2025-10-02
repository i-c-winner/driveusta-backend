from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.dependencies import get_db
from app.db.repositories.calendar.working_hours import WorkingHourRepository
from app.schemas.calendar.working_hours import WorkingHourResponse, WorkingHoursListResponse, WorkingHourCreate, WorkingHourUpdate

router = APIRouter(
    prefix="/calendar/working-hours",
    tags=["calendar", "working-hours"]
)

@router.post("/", response_model=WorkingHourResponse)
async def create_working_hour(working_hour: WorkingHourCreate, db: Session = Depends(get_db)):
    """
    Создать новую запись рабочих часов
    """
    try:
        working_hour_repo = WorkingHourRepository(db)
        new_working_hour = working_hour_repo.create_working_hour(working_hour)
        
        working_hour_response = WorkingHourResponse.model_validate(new_working_hour)
        return working_hour_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании записи: {str(e)}")

@router.get("/", response_model=WorkingHoursListResponse)
async def get_working_hours(db: Session = Depends(get_db)):
    """
    Получить список всех рабочих часов из базы данных
    """
    try:
        working_hour_repo = WorkingHourRepository(db)
        working_hours = working_hour_repo.get_all_working_hours()
        
        # Преобразуем модели SQLAlchemy в схемы Pydantic
        working_hour_responses = [WorkingHourResponse.model_validate(working_hour) for working_hour in working_hours]
        
        return WorkingHoursListResponse(working_hours=working_hour_responses)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@router.get("/{working_hour_id}", response_model=WorkingHourResponse)
async def get_working_hour_by_id(working_hour_id: int, db: Session = Depends(get_db)):
    """
    Получить рабочие часы по ID
    """
    try:
        working_hour_repo = WorkingHourRepository(db)
        working_hour = working_hour_repo.get_working_hour_by_id(working_hour_id)
        
        if working_hour is None:
            raise HTTPException(status_code=404, detail=f"Рабочие часы с ID {working_hour_id} не найдены")
        
        working_hour_response = WorkingHourResponse.model_validate(working_hour)
        return working_hour_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@router.put("/{working_hour_id}", response_model=WorkingHourResponse)
async def update_working_hour(working_hour_id: int, working_hour: WorkingHourUpdate, db: Session = Depends(get_db)):
    """
    Обновить рабочие часы по ID
    """
    try:
        working_hour_repo = WorkingHourRepository(db)
        updated_working_hour = working_hour_repo.update_working_hour(working_hour_id, working_hour)
        
        if updated_working_hour is None:
            raise HTTPException(status_code=404, detail=f"Рабочие часы с ID {working_hour_id} не найдены")
        
        working_hour_response = WorkingHourResponse.model_validate(updated_working_hour)
        return working_hour_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении данных: {str(e)}")

@router.delete("/{working_hour_id}")
async def delete_working_hour(working_hour_id: int, db: Session = Depends(get_db)):
    """
    Удалить рабочие часы по ID
    """
    try:
        working_hour_repo = WorkingHourRepository(db)
        result = working_hour_repo.delete_working_hour(working_hour_id)
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Рабочие часы с ID {working_hour_id} не найдены")
        
        return {"message": f"Рабочие часы с ID {working_hour_id} успешно удалены"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении данных: {str(e)}")