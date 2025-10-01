from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Cars(Base):
    __tablename__ = "cars"
    __table_args__ = {"schema": "cars"}
    
    id = Column(Integer, primary_key=True, index=True)
    car_name = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    model = Column(String, nullable=True)
    year = Column(Integer, nullable=True)

    # Обратная связь
    participants = relationship('Participants', back_populates='car')