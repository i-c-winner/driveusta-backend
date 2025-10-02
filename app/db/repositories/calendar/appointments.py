from sqlalchemy.orm import Session
from app.models.calendar.appointments import Appointments
from app.schemas.calendar.appointments import AppointmentCreate, AppointmentUpdate
from typing import List


class AppointmentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_appointments(self, work_shop_id: int) -> List[Appointments]:
        """Получить все записи на прием из базы данных для определенного СТО"""
        return self.db.query(Appointments).filter(Appointments.work_shop_id == work_shop_id).all()
    
    def get_appointment_by_id(self, appointment_id: int, work_shop_id: int) -> Appointments:
        """Получить запись на прием по ID для определенного СТО"""
        return self.db.query(Appointments).filter(
            Appointments.id == appointment_id,
            Appointments.work_shop_id == work_shop_id
        ).first()
    
    def create_appointment(self, appointment: AppointmentCreate) -> Appointments:
        """Создать новую запись на прием"""
        db_appointment = Appointments(
            work_shop_id=appointment.work_shop_id,
            client_name=appointment.client_name,
            client_phone=appointment.client_phone,
            car_license_plate=appointment.car_license_plate,
            appointment_date=appointment.appointment_date,
            appointment_time=appointment.appointment_time,
            duration_minutes=appointment.duration_minutes,
            time=appointment.time,
            description=appointment.description
        )
        self.db.add(db_appointment)
        self.db.commit()
        self.db.refresh(db_appointment)
        return db_appointment
    
    def update_appointment(self, appointment_id: int, work_shop_id: int, appointment: AppointmentUpdate) -> Appointments:
        """Обновить запись на прием для определенного СТО"""
        db_appointment = self.get_appointment_by_id(appointment_id, work_shop_id)
        if db_appointment:
            update_data = appointment.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_appointment, key, value)
            self.db.commit()
            self.db.refresh(db_appointment)
        return db_appointment
    
    def delete_appointment(self, appointment_id: int, work_shop_id: int) -> bool:
        """Удалить запись на прием для определенного СТО"""
        db_appointment = self.get_appointment_by_id(appointment_id, work_shop_id)
        if db_appointment:
            self.db.delete(db_appointment)
            self.db.commit()
            return True
        return False