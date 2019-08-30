from pydantic import BaseModel
from datetime import datetime
from typing import Dict

class KitCreate(BaseModel):
    serial: str = None
    id: int = 0


class KitUpdate(KitCreate):
    kit_id: int


class KitFullModel(KitUpdate):
    created_at: datetime = datetime.now()
    location: Dict = {}
