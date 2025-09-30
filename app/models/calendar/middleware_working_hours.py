from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base

class MiddlewareWorkingHours(Base):
    __tablename__ = "middleware_working_hours"

    id=Column(Integer, primary_key=True, index=True)
    working_hours_id=Column(Integer, ForeignKey("working_hours.id"))
    work_shop_id=Column(Integer, ForeignKey("work_shop.id"))

    work_shop=relationship('work_shop', backref='middleware_working_hours')
    working_hours=relationship('working_hours', backref='middleware_working_hours')