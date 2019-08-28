from pydantic import BaseModel
from datetime import datetime


class KitCreate(BaseModel):
    serial: str = None
    created_at: datetime = datetime.now()
    longitude: float = None
    latitude: float = None


class KitUpdate(KitCreate):
    kit_id: int


class KitModel(KitUpdate):
    pass
