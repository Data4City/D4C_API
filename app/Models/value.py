from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from Models import Base

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
