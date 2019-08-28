from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship, backref

from db_models.manyToManyRelationships import values_from_sensor, measurements_in_sensor

from app.db.base_class import Base


class Sensor(Base):
    __tablename__ = "sensor"
    id = Column('id', Integer, primary_key=True)
    name = Column("name", String(40), nullable=False)
    model = Column("model", String(40), nullable=False)
    measurements = relationship('Measurement', secondary=measurements_in_sensor,
                                backref=backref('sensors', lazy='dynamic'))
    values = relationship("Value", secondary=values_from_sensor)

    @property
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'measurements': [m.as_simple_dict for m in self.measurements]
        }

    def add_kit(self, kit, session):
        self.kits.append(kit)
        session.commit()

    def save(self, session):
        session.add(self)
        session.commit()
