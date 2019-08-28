from sqlalchemy.orm import Session
from db_models.kit import Kit
from typing import List, Optional


def get(db_session: Session, *, kit_id: int):
    return db_session.query(Kit).get(kit_id).first()


def get_multi(db_session: Session, *, limit=10) -> List[Optional[Kit]]:
    return db_session.query(Kit).limit(limit).all()


