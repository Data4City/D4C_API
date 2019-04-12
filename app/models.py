from datetime import datetime

from sqlalchemy import create_engine, Table, Column, String, Integer, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

sensors_in_kit = Table('sensors_in_kit', Base.metadata,
                       Column('kit_id', Integer, ForeignKey('kit.id')),
                       Column('sensor_id', Integer, ForeignKey('sensor.id')))

measurements_in_sensor = Table('measurements_in_sensor', Base.metadata,
                               Column('sensor_id', Integer, ForeignKey('sensor.id')),
                               Column('measurement_id', Integer, ForeignKey('measurement.id')))


class Kit(Base):
    __tablename__ = "kit"
    # TODO Add geolocation
    id = Column('id', Integer, primary_key=True)
    serial = Column('serial', String(16))
    created_at = Column("timestamp", DateTime(timezone=True), default=datetime.now())
    sensors_used = relationship('Sensor', secondary=sensors_in_kit, backref=backref('kits', lazy='dynamic'))
    values = relationship("Value", back_populates="kit")

    def __init__(self, serial):
        self.serial = serial

    @property
    def as_dict(self):
        return {
            'id': self.id,
            'serial': self.serial,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'sensors_used': [s.as_dict for s in self.sensors_used]
        }

    def save(self, session):
        session.add(self)
        session.commit()


class Sensor(Base):
    __tablename__ = "sensor"
    id = Column('id', Integer, primary_key=True)
    name = Column("name", String(40), nullable=False)
    model = Column("model", String(40), nullable=False)
    measurements = relationship('Measurement', secondary=measurements_in_sensor,
                                backref=backref('sensors', lazy='dynamic'))

    @property
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'measurements': [m.as_dict for m in self.measurements]
        }

    def add_kit(self, kit, session):
        self.kits.append(kit)
        session.commit()

    def save(self, session):
        session.add(self)
        session.commit()


class Measurement(Base):
    __tablename__ = "measurement"
    id = Column('id', Integer, primary_key=True)
    symbol = Column('symbol', String(10))
    name = Column('name', String(30))

    @property
    def as_dict(self):
        return {
            'symbol': self.symbol,
            'name': self.name,
            "id": self.id
        }

    def add_sensor(self, sensor, session):
        self.sensors.append(sensor)
        session.commit()

    def save(self, session):
        session.add(self)
        session.commit()


class Value(Base):
    __tablename__ = "value"
    id = Column('id', Integer, primary_key=True)
    data = Column("data", Float)
    timestamp = Column("timestamp", DateTime(timezone=True))
    measurement_id = Column('measurement_id', Integer, ForeignKey('measurement.id'))
    kit_id = Column('kit_id', Integer, ForeignKey('kit.id'))
    kit = relationship("Kit", back_populates="values")

    def __init__(self, data, timestamp, kit, measurement):
        self.data = data
        self.timestamp = timestamp
        self.kit_id = kit
        self.measurement_id = measurement

    @property
    def as_dict(self):
        return {
            'timestamp': self.timestamp,
            'data': self.data,
            'symbol': self.measurement.symbol
        }

    def save(self, session):
        session.add(self)


def __reset_db__():
    engine = create_engine("sqlite:///sensor.db", echo=True)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    __reset_db__()
