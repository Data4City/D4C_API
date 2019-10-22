from datetime import datetime
from typing import Dict

from .dbmodel import DBModelMixin


class KitCreate(DBModelMixin):
    serial: str = None
    id: int = 0


class KitUpdate(DBModelMixin):
    longitude: float = None
    latitude: float = None


class KitFullModel(KitCreate):
    created_at: datetime = datetime.now()
    location: Dict = {}
