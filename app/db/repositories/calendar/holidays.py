from sqlalchemy.orm import Session
from app.models.calendar.holidays import Holidays
from app.schemas.calendar.holidays import HolidayCreate, HolidayUpdate
from typing import List


class HolidayRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_holidays(self, work_shop_id: int) -> List[Holidays]:
        """Получить все праздники из базы данных для определенного СТО"""
        return self.db.query(Holidays).filter(Holidays.work_shop_id == work_shop_id).all()
    
    def get_holiday_by_id(self, holiday_id: int, work_shop_id: int) -> Holidays:
        """Получить праздник по ID для определенного СТО"""
        return self.db.query(Holidays).filter(
            Holidays.id == holiday_id,
            Holidays.work_shop_id == work_shop_id
        ).first()
    
    def create_holiday(self, holiday: HolidayCreate) -> Holidays:
        """Создать новый праздник"""
        db_holiday = Holidays(
            work_shop_id=holiday.work_shop_id,
            description=holiday.description
        )
        self.db.add(db_holiday)
        self.db.commit()
        self.db.refresh(db_holiday)
        return db_holiday
    
    def update_holiday(self, holiday_id: int, work_shop_id: int, holiday: HolidayUpdate) -> Holidays:
        """Обновить праздник для определенного СТО"""
        db_holiday = self.get_holiday_by_id(holiday_id, work_shop_id)
        if db_holiday:
            update_data = holiday.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_holiday, key, value)
            self.db.commit()
            self.db.refresh(db_holiday)
        return db_holiday
    
    def delete_holiday(self, holiday_id: int, work_shop_id: int) -> bool:
        """Удалить праздник для определенного СТО"""
        db_holiday = self.get_holiday_by_id(holiday_id, work_shop_id)
        if db_holiday:
            self.db.delete(db_holiday)
            self.db.commit()
            return True
        return False