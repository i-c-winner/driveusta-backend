from sqlalchemy.orm import Session
from app.models.calendar.holidays import Holidays
from app.schemas.calendar.holidays import HolidayCreate, HolidayUpdate
from typing import List


class HolidayRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_holidays(self) -> List[Holidays]:
        """Получить все праздники из базы данных"""
        return self.db.query(Holidays).all()
    
    def get_holiday_by_id(self, holiday_id: int) -> Holidays:
        """Получить праздник по ID"""
        return self.db.query(Holidays).filter(Holidays.id == holiday_id).first()
    
    def create_holiday(self, holiday: HolidayCreate) -> Holidays:
        """Создать новый праздник"""
        db_holiday = Holidays(
            description=holiday.description
        )
        self.db.add(db_holiday)
        self.db.commit()
        self.db.refresh(db_holiday)
        return db_holiday
    
    def update_holiday(self, holiday_id: int, holiday: HolidayUpdate) -> Holidays:
        """Обновить праздник"""
        db_holiday = self.get_holiday_by_id(holiday_id)
        if db_holiday:
            update_data = holiday.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_holiday, key, value)
            self.db.commit()
            self.db.refresh(db_holiday)
        return db_holiday
    
    def delete_holiday(self, holiday_id: int) -> bool:
        """Удалить праздник"""
        db_holiday = self.get_holiday_by_id(holiday_id)
        if db_holiday:
            self.db.delete(db_holiday)
            self.db.commit()
            return True
        return False