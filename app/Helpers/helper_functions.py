from typing import Dict


# Returns a boolean if the instance was created.
def get_or_create(session, dbModel, **kwargs):
    instance = session.query(dbModel).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = dbModel(**kwargs)
        session.add(instance)
        session.commit()
        return instance, True


def res_to_json(res_object):
    to_return = {}
    for idx, val in enumerate(res_object._fields):
        to_return[val] = res_object[idx]
    return to_return
# Filters incoming put requests so only the necessary fields are considered
def filter_request(model, request: Dict) -> Dict:
    to_return = {}
    for k, v in request.items():
        if k in model.__table__.columns.keys():
            to_return[k] = v

    return to_return


def get_env_variable(name) -> str:
    import os
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


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
