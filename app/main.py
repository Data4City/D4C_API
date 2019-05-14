import logging

import falcon
from falcon import API
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

import routes
from Helpers.Middlewares import SQLAlchemySessionManager, Jsonify, ResponseLoggerMiddleware
from Helpers.helper_functions import create_db_connection_url

logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler('api.log'))
logger.setLevel(logging.INFO)


def get_app() -> API:
    engine = create_engine(create_db_connection_url(), echo=True)
    if not database_exists(engine.url):
        create_database(engine.url)
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)

    _app = falcon.API(middleware=[SQLAlchemySessionManager(Session), Jsonify.Middleware(help_messages=True),
                                  ResponseLoggerMiddleware()])

    routes.add_routes(_app)

    return _app


app = get_app()
