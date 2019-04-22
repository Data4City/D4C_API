import falcon
from falcon import API
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from Helpers.Middlewares import SQLAlchemySessionManager, Jsonify, ResponseLoggerMiddleware
from Helpers.helper_functions import create_db_connection_url
from Resources import *

engine = create_engine(create_db_connection_url())

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


def get_app() -> API:
    _app = falcon.API(middleware=[SQLAlchemySessionManager(Session), Jsonify.Middleware(help_messages=True), ResponseLoggerMiddleware()])
    _app.add_route('/v1/kit', KitResource())
    _app.add_route('/v1/{kit_id:int}/kit', GeneralKitResource())
    _app.add_route('/v1/{kit_id:int}/sensor', SensorResource())
    _app.add_route('/v1/{kit_id:int}/measurement', MeasurementResource())
    _app.add_route('/v1/{kit_id:int}/values', ValueResource)
    return _app
