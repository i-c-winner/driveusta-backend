from sqlalchemy.orm import Session
from app.models.calendar.working_hours import WorkingHours
from app.schemas.calendar.working_hours import WorkingHourCreate, WorkingHourUpdate
from typing import List


class WorkingHourRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_working_hours(self, work_shop_id: int) -> List[WorkingHours]:
        """Получить все рабочие часы из базы данных для определенного СТО"""
        return self.db.query(WorkingHours).filter(WorkingHours.work_shop_id == work_shop_id).all()
    
    def get_working_hour_by_id(self, working_hour_id: int, work_shop_id: int) -> WorkingHours:
        """Получить рабочие часы по ID для определенного СТО"""
        return self.db.query(WorkingHours).filter(
            WorkingHours.id == working_hour_id,
            WorkingHours.work_shop_id == work_shop_id
        ).first()
    
    def create_working_hour(self, working_hour: WorkingHourCreate) -> WorkingHours:
        """Создать новую запись рабочих часов"""
        db_working_hour = WorkingHours(
            work_shop_id=working_hour.work_shop_id,
            day_of_week=working_hour.day_of_week,
            is_working=working_hour.is_working,
            opening_time=working_hour.opening_time,
            closing_time=working_hour.closing_time
        )
        self.db.add(db_working_hour)
        self.db.commit()
        self.db.refresh(db_working_hour)
        return db_working_hour
    
    def update_working_hour(self, working_hour_id: int, work_shop_id: int, working_hour: WorkingHourUpdate) -> WorkingHours:
        """Обновить запись рабочих часов для определенного СТО"""
        db_working_hour = self.get_working_hour_by_id(working_hour_id, work_shop_id)
        if db_working_hour:
            update_data = working_hour.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_working_hour, key, value)
            self.db.commit()
            self.db.refresh(db_working_hour)
        return db_working_hour
    
    def delete_working_hour(self, working_hour_id: int, work_shop_id: int) -> bool:
        """Удалить запись рабочих часов для определенного СТО"""
        db_working_hour = self.get_working_hour_by_id(working_hour_id, work_shop_id)
        if db_working_hour:
            self.db.delete(db_working_hour)
            self.db.commit()
            return True
        return False