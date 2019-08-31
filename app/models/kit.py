from pydantic import BaseModel
from datetime import datetime
from typing import Dict


class KitCreate(BaseModel):
    serial: str = None
    id: int = 0


class KitUpdate(BaseModel):
    longitude: float = None
    latitude: float = None


class KitFullModel(KitCreate) :
    created_at: datetime = datetime.now()
    location: Dict = {}
