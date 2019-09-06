from sqlalchemy import Column, Integer, LargeBinary
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class DBFile(Base):
    id = Column('id', Integer, primary_key=True)
    data = Column('data', LargeBinary, unique=True)
    # inferences = relationship("Inference")
