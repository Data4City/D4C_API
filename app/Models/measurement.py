from sqlalchemy import Column, String, Integer

from . import Base


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
