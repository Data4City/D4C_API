from enum import Enum

from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy import Enum as EnumDB
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class LabelsEnum(Enum):
    air_conditioner = 0
    car_horn = 1
    children_playing = 2
    dog_bark = 3
    drilling = 4
    engine_idling = 5
    gun_shot = 6
    jackhammer = 7
    siren = 8
    street_music = 9


class Labels(Base):
    id = Column(Integer, primary_key=True)
    label = Column(EnumDB(LabelsEnum))
    dataset_entry = relationship("DBFile")


class Inference(Base):
    id = Column('id', Integer, primary_key=True)
    accuracy = Column('accuracy', Float)
    model_used = Column(String(40), nullable=False)
    file_id = Column(Integer, ForeignKey('dbfile.id'))
    predicted_label = Column(Integer, ForeignKey("labels.id"))
