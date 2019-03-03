import falcon
from falcon import API
from Resources import *
from Helpers.middlewares import SQLAlchemySessionManager
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///sensor.db")#, echo=True)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


def get_app() -> API:
    _app = falcon.API(middleware=[SQLAlchemySessionManager(Session)])
    _app.add_route('/v1/kit', KitResource())
    _app.add_route('/v1/sensor', SensorResource())
    return _app
