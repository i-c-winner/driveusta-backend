from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base

class MiddlewareHoliday(Base):
    __tablename__ = "middleware_holiday"
    id=Column(Integer, primary_key=True, index=True)
    holiday_date_id=Column(Integer, ForeignKey("holidays.id"))

    work_shop= relationship('work_shop', backref='middleware_holiday')
    holiday= relationship('holidays', backref='middleware_holiday')