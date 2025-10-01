from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base

class TypeWorkChildren(Base):
    __tablename__ = "type_work_children"
    __table_args__ = {"schema": "cars"}

    id = Column(Integer, primary_key=True, index=True)
    type_work_child_name = Column(String)
    parent_id = Column(Integer, ForeignKey("cars.type_work_parents.id"))

    parent=relationship('TypeWorkParents', backref='children')
    appointments = relationship('Appointments', secondary='participants.appointments_work_type_children', back_populates='work_type')