from typing import Dict


def get_or_create(session, dbModel, **kwargs):
    instance = session.query(dbModel).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = dbModel(**kwargs)
        session.add(instance)
        session.commit()
        return instance


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
    return 'postgresql+pg8000://{user}:{pw}@{url}/{db}'.format(user=get_env_variable("POSTGRES_USER"), pw=get_env_variable("POSTGRES_PW"), url=get_env_variable("POSTGRES_URL"),
                                                        db=get_env_variable("POSTGRES_DB"))
