from sqlalchemy import Column, Integer, String
from app.db.base import Base

class TypeWorkParents(Base):
    __tablename__ = "type_work_parents"

    id = Column(Integer, primary_key=True, index=True)
    type_work_parent_name = Column(String)