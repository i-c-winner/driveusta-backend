from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base

class Streets(Base):
    __tablename__ = "streets"
    id = Column(Integer, primary_key=True, index=True)
    street_name = Column(String, nullable=True)
    id_sto = Column(Integer, ForeignKey("sto.id"))

    sto=relationship('Sto', backref='streets')