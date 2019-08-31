from datetime import datetime

from geoalchemy2.shape import from_shape, to_shape
from geoalchemy2.types import Geometry
from shapely.geometry import Point, mapping
from sqlalchemy import Column, String, Integer, DateTime

from app.db.base_class import Base


class Kit(Base):
    id = Column('id', Integer, primary_key=True)
    serial = Column('serial', String)
    created_at = Column("timestamp", DateTime(timezone=True), default=datetime.now())
    geom = Column(Geometry(geometry_type='POINT', srid=4326))

    # sensors_used = relationship('Sensor', secondary=sensors_in_kit, backref=backref('kits', lazy='dynamic'))
    # values = relationship("Value", secondary=values_from_sensor)

    def __init__(self, serial):
        self.serial = serial

    def set_location(self, long, lat):
        p = Point(long, lat)
        self.geom = from_shape(p, srid=4326)

    @property
    def as_complete_dict(self):
        return {
            'kit_id': self.id,
            'serial': self.serial,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'location': self.get_position()
        }

    @property
    def as_simple_dict(self):
        return {
            'kit_id': self.id,
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
