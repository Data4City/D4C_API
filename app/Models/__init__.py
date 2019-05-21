from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from Helpers.helper_functions import create_db_connection_url

Base = declarative_base()

from Models.kit import Kit
from Models.measurement import Measurement
from Models.sensor import Sensor
from Models.value import Value


def reset_db():
    engine = create_engine(create_db_connection_url(), echo=True)
    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
