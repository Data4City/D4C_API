from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.api.utils.db import create_db_connection_url
from app.core import config

engine = create_engine(create_db_connection_url, pool_pre_ping=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
