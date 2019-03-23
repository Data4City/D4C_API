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
