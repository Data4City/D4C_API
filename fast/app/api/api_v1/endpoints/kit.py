from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_200_OK
from starlette.responses import Response

from app.api.utils.db import get_db
from app.crud import kit as crud_kit
from app.models.kit import KitFullModel

router = APIRouter()


@router.get("/", response_model=KitFullModel, status_code=HTTP_200_OK)
def get_single_kit(*, db: Session = Depends(get_db), kit_id: int):
    return crud_kit.get(db, kit_id=kit_id)


@router.post("/", response_model=KitFullModel, status_code=HTTP_201_CREATED)
def create_single_kit(*, db: Session = Depends(get_db), serial: str, response: Response):
    kit, created = crud_kit.create_single(db, serial=serial)

    if not created:
        response.status_code = HTTP_200_OK

    return kit.as_complete_dict
