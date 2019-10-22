from enum import Enum

from sqlalchemy import Column, String, Integer, Float, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Label(Base):
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, unique=True, index=True)
    dataset_entry = relationship("DBFile", backref="label")


class Inference(Base):
    id = Column('id', Integer, primary_key=True)
    accuracy = Column('accuracy', Float)
    model_used = Column(String(40), nullable=False)
    file_id = Column(Integer, ForeignKey('dbfile.id'))
    predicted_label = Column(Integer, ForeignKey("label.id"))


class DBFile(Base):
    id = Column('id', Integer, primary_key=True)
    data = Column('data', LargeBinary, nullable=False, unique=True)
    label_id = Column(Integer, ForeignKey("label.id"))
    # inferences = relationship("Inference")

