from urllib.parse import uses_relative

from sqlalchemy.orm import Session
from app.models.calendar.appointments import Appointments
from app.schemas.calendar.appointments import AppointmentCreate, AppointmentUpdate
from typing import List

from app.services.security.auth.token import get_current_username


class AppointmentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_appointment_by_username(self, username: str) -> Appointments:
        """Получить запись на прием по ID для определенного СТО"""
        return self.db.query(Appointments).filter(
            Appointments.work_shop_username == username).all()
    def get_appointment_by_id(self, id) -> Appointments:
        return self.db.query(Appointments).filter(Appointments.id == id).first()
    def create_appointment(self, appointment: AppointmentCreate) -> Appointments:
        """Создать новую запись на прием"""
        db_appointment = Appointments(
            work_shop_username=appointment.work_shop_username,
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
    
    def update_appointment(self, id: int,  appointment: AppointmentUpdate, username: str) -> Appointments:
        """Обновить запись на прием для определенного СТО"""
        username = get_current_username(username)
        db_appointments = self.get_appointment_by_username(username)
        db_appointment_id = list(filter(lambda x: x.id==id), db_appointments)
        if db_appointment_id:
            update_data = appointment.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_appointment_id, key, value)
            self.db.commit()
            self.db.refresh(db_appointment_id)
        return db_appointment_id
    
    # def delete_appointment(self, appointment_id: int, work_shop_username: str) -> bool:
    #     """Удалить запись на прием для определенного СТО"""
    #     db_appointment = self.get_appointment_by_id(appointment_id, work_shop_username)
    #     if db_appointment:
    #         self.db.delete(db_appointment)
    #         self.db.commit()
    #         return True
    #     return False