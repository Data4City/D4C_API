from sqlalchemy.orm import Session
from app.db_models.kit import Kit
from typing import List, Optional, Tuple
from app.db.helpers import get_or_create


def get_single(db_session: Session, *, kit_id: int) -> Kit:
    return db_session.query(Kit).get(kit_id)


def get_multi(db_session: Session, *, amount=10) -> List[Optional[Kit]]:
    return db_session.query(Kit).limit(amount).all()


def create_single(db_session: Session, *, serial: str) -> Tuple[Kit, bool]:
    return get_or_create(db_session, Kit, serial=serial)
