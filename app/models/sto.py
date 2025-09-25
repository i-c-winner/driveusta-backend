from sqlalchemy import Column, Integer, String, Numeric, Float
from app.db.base import Base

class Sto(Base):
    __tablename__ = "sto"

    id = Column(Integer, primary_key=True, index=True)
    sto_name = Column(String, nullable=True)
    telephone = Column(String, nullable=True)
    street_name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    site = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
