from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.dependencies import get_db
from app.db.repositories.calendar.appointments import AppointmentRepository
from app.schemas.calendar.appointments import AppointmentResponse, AppointmentsListResponse, AppointmentCreate, AppointmentUpdate

router = APIRouter(
    prefix="/calendar/appointments",
    tags=["calendar", "appointments"]
)

@router.post("/", response_model=AppointmentResponse)
async def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    """
    Создать новую запись на прием
    """
    try:
        appointment_repo = AppointmentRepository(db)
        new_appointment = appointment_repo.create_appointment(appointment)
        
        appointment_response = AppointmentResponse.model_validate(new_appointment)
        return appointment_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании записи: {str(e)}")

@router.get("/", response_model=AppointmentsListResponse)
async def get_appointments(work_shop_username: int, db: Session = Depends(get_db)):
    """
    Получить список всех записей на прием из базы данных для определенного СТО
    """
    try:
        appointment_repo = AppointmentRepository(db)
        appointments = appointment_repo.get_all_appointments(work_shop_username)
        
        # Преобразуем модели SQLAlchemy в схемы Pydantic
        appointment_responses = [AppointmentResponse.model_validate(appointment) for appointment in appointments]
        
        return AppointmentsListResponse(appointments=appointment_responses)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@router.get("/{username}", response_model=AppointmentResponse)
async def get_appointment_by_username(username: str, db: Session = Depends(get_db)):
    """
    Получить запись на прием по ID для определенного СТО
    """
    try:
        appointment_repo = AppointmentRepository(db)
        appointment = appointment_repo.get_appointment_by_username(username)
        
        if appointment is None:
            raise HTTPException(status_code=404, detail=f"Запись на прием  для СТО {username} не найдена")
        
        appointment_response = AppointmentResponse.model_validate(appointment)
        return appointment_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")

@router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(appointment_id: int, work_shop_id: int, appointment: AppointmentUpdate, db: Session = Depends(get_db)):
    """
    Обновить запись на прием по ID для определенного СТО
    """
    try:
        appointment_repo = AppointmentRepository(db)
        updated_appointment = appointment_repo.update_appointment(appointment_id, work_shop_id, appointment)
        
        if updated_appointment is None:
            raise HTTPException(status_code=404, detail=f"Запись на прием с ID {appointment_id} для СТО {work_shop_id} не найдена")
        
        appointment_response = AppointmentResponse.model_validate(updated_appointment)
        return appointment_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении данных: {str(e)}")

@router.delete("/{appointment_id}")
async def delete_appointment(appointment_id: int, work_shop_id: int, db: Session = Depends(get_db)):
    """
    Удалить запись на прием по ID для определенного СТО
    """
    try:
        appointment_repo = AppointmentRepository(db)
        result = appointment_repo.delete_appointment(appointment_id, work_shop_id)
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Запись на прием с ID {appointment_id} для СТО {work_shop_id} не найдена")
        
        return {"message": f"Запись на прием с ID {appointment_id} для СТО {work_shop_id} успешно удалена"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении данных: {str(e)}")