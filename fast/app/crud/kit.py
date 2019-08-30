from sqlalchemy.orm import Session
from app.db_models.kit import Kit
from typing import List, Optional
from app.db.helpers import get_or_create


def get_single(db_session: Session, *, kit_id: int):
    return db_session.query(Kit).get(kit_id).first()


def get_multi(db_session: Session, *, limit=10) -> List[Optional[Kit]]:
    return db_session.query(Kit).limit(limit).all()


def create_single(db_session: Session, *, serial: str):
    return get_or_create(db_session, Kit, serial=serial)
