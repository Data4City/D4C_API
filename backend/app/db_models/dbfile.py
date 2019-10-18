from sqlalchemy import Column, Integer, LargeBinary
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from sqlalchemy import Enum as EnumDB
from .inference import  LabelsEnum

class DBFile(Base):
    id = Column('id', Integer, primary_key=True)
    data = Column('data', LargeBinary, nullable=False)
    label = Column(EnumDB(LabelsEnum))
    inferences = relationship("Inference")
