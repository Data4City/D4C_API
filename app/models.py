from datetime import datetime

from sqlalchemy import create_engine, Table, Column, String, Integer, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import database_exists, create_database
from geoalchemy2.types import Geometry
from shapely.geometry import Point, mapping
from geoalchemy2.shape import from_shape, to_shape
from Helpers.helper_functions import create_db_connection_url

Base = declarative_base()

sensors_in_kit = Table('sensors_in_kit', Base.metadata,
                       Column('kit_id', Integer, ForeignKey('kit.id')),
                       Column('sensor_id', Integer, ForeignKey('sensor.id')))

measurements_in_sensor = Table('measurements_in_sensor', Base.metadata,
                               Column('sensor_id', Integer, ForeignKey('sensor.id')),
                               Column('measurement_id', Integer, ForeignKey('measurement.id')))

values_from_sensor = Table('values_from_sensor', Base.metadata,
                           Column('kit_id', Integer, ForeignKey('kit.id')),
                           Column('sensor_id', Integer, ForeignKey('sensor.id')),
                           Column('value_id', Integer, ForeignKey('value.id'))
                           )


class Kit(Base):
    __tablename__ = "kit"

    id = Column('id', Integer, primary_key=True)
    serial = Column('serial', String)
    created_at = Column("timestamp", DateTime(timezone=True), default=datetime.now())
    geom = Column(Geometry(geometry_type='POINT', srid=4326))

    sensors_used = relationship('Sensor', secondary=sensors_in_kit, backref=backref('kits', lazy='dynamic'))
    values = relationship("Value", secondary=values_from_sensor)

    def __init__(self, serial):
        self.serial = serial

    def set_location(self, lat, long):
        p = Point(long, lat)
        self.geom = from_shape(p, srid=4326)

    @property
    def as_complete_dict(self):
        return {
            'id': self.id,
            'serial': self.serial,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'sensors_used': [s.as_dict for s in self.sensors_used]
            'location': self.get_position()
        }

    @property
    def as_simple_dict(self):
        return {
            'id': self.id,
            'serial': self.serial,
            'location': self.get_position()

        }

    def get_position(self):
        try:
            return mapping(to_shape(self.geom))
        except Exception:
            return {}

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


class Measurement(Base):
    __tablename__ = "measurement"
    id = Column('id', Integer, primary_key=True)
    symbol = Column('symbol', String(10))
    name = Column('name', String(30))

    @property
    def as_simple_dict(self):
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
    measurement_id = ('Measurement', Integer, ForeignKey('measurement.id'))

    # kit_id = Column('kit_id', Integer, ForeignKey('kit.id'))
    # kit = relationship("Kit", back_populates="values")

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
            'symbol': self.measurement_id.symbol,
            'id': self.id
        }

    def save(self, session):
        session.add(self)


def __reset_db__():
    engine = create_engine(create_db_connection_url(), echo=True)
    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    __reset_db__()
