from .dbmodel import DBModelMixin


class Label(DBModelMixin):
    label: str
    id: int
