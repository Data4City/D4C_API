from starlette.requests import Request
from app.api.utils.general import get_env_variable


def get_db(request: Request):
    return request.state.db


def create_db_connection_url():
    conn = ""
    try:
        import psycopg2cffi
        conn = 'postgresql+psycopg2cffi://{user}:{pw}@{url}/{db}'.format(user=get_env_variable("POSTGRES_USER"),
                                                                         pw=get_env_variable("POSTGRES_PASS"),
                                                                         url=get_env_variable("POSTGRES_URL"),
                                                                         db=get_env_variable("POSTGRES_DBNAME"))
    except ModuleNotFoundError:
        conn = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=get_env_variable("POSTGRES_USER"),
                                                                     pw=get_env_variable("POSTGRES_PASS"),
                                                                     url=get_env_variable("POSTGRES_URL"),
                                                                     db=get_env_variable("POSTGRES_DBNAME"))
    print(conn)
    return conn
