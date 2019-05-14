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


def get_app() -> API:
    engine = create_engine(create_db_connection_url())
    if not database_exists(engine.url):
        logger.info("Creating database")
        create_database(engine.url)
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)

    _app = falcon.API(middleware=[SQLAlchemySessionManager(Session), Jsonify.Middleware(help_messages=True),
                                  ResponseLoggerMiddleware()])

    routes.add_routes(_app)

    return _app


FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger("mainapp." + __name__)
gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)
app = get_app()
