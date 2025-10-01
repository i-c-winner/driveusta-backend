from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Time
from datetime import time

from sqlalchemy.orm import relationship

from app.db.base import Base


class WorkingHours(Base):
    __tablename__ = "working_hours"
    __table_args__ = {"schema": "work_shop"}

    id=Column(Integer, primary_key=True, index=True)
    work_shop_id=Column(Integer, ForeignKey("work_shop.work_shop.id"))
    day_of_week=Column(Integer, nullable=True)
    is_working=Column(Boolean, nullable=True)
    opening_time=Column(Time, default=time(8, 0),nullable= True)
    closening_time=Column(String, default=time(20, 0), nullable=True)

    work_shop=relationship('work_shop', backref='working_hours')