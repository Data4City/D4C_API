import falcon
from falcon import API
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from Helpers.Middlewares import SQLAlchemySessionManager, Jsonify, ResponseLoggerMiddleware
from Resources import *

engine = create_engine("sqlite:///sensor.db")#, echo=True)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


def get_app() -> API:
    _app = falcon.API(middleware=[SQLAlchemySessionManager(Session), Jsonify.Middleware(help_messages=True), ResponseLoggerMiddleware()])
    _app.add_route('/v1/kit', KitResource())
    _app.add_route('/v1/sensor', SensorResource())
    _app.add_route('/v1/measurement', MeasurementResource())
    _app.add_route('/v1/i2c', ValueResource())
    return _app
