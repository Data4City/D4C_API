
from sqlalchemy import Table, Column, Integer, ForeignKey

from Models import Base
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
