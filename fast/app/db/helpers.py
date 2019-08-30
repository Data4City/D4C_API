from typing import Tuple


# Returns a boolean if the instance was created.
def get_or_create(session, dbModel, **kwargs) -> Tuple:
    instance = session.query(dbModel).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = dbModel(**kwargs)
        session.add(instance)
        session.commit()
        return instance, True
