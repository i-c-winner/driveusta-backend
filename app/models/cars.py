from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Cars(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    car_name = Column(String, nullable=True)
    sto_id = Column(Integer, ForeignKey("sto.id"))