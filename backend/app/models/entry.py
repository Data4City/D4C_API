from typing import Optional

from .dbmodel import DBModelMixin


class Entry(DBModelMixin):
    label_id: Optional[int]
    data: bytes

