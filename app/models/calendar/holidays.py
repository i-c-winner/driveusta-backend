from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base

class Holidays(Base):
    __tablename__ = "holidays"
    __table_args__ = {"schema": "work_shop"}

    id=Column(Integer, primary_key=True, index=True)
    description=Column(String(200), nullable=False)

    work_shop=relationship('work_shop', secondary="work_shop.holidays_work_shops", back_populates="holidays")