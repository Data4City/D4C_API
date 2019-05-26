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
        from Models import Base
        logging.getLogger("mainapp." + __name__).info("Creating database")
        create_database(engine.url)
        Base.metadata.create_all(bind=engine)

    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)

    _app = falcon.API(middleware=[SQLAlchemySessionManager(Session), Jsonify.Middleware(help_messages=True),
                                  ResponseLoggerMiddleware()])

    routes.add_routes(_app)

    return _app


def speed_up_logs():
    from logging.handlers import QueueHandler, QueueListener

    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    rootLogger = logging.getLogger("mainapp." + __name__)

    from Helpers.EvictQueue import EvictQueue
    log_que = EvictQueue(1000)
    queue_handler = QueueHandler(log_que)
    queue_listener =QueueListener(log_que, *rootLogger.handlers)
    queue_listener.start()

    gunicorn_logger = logging.getLogger('gunicorn.error')
    rootLogger.setLevel(gunicorn_logger.level)
    rootLogger.handlers = [queue_handler, gunicorn_logger.handlers]

speed_up_logs()
app = get_app()
