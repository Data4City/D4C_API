from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST
from starlette.responses import Response

from app.api.utils.db import get_db
from app.crud import kit as crud_kit
from app.models.kit import KitFullModel, KitUpdate
from app.db_models.kit import Kit as KitInDB

router = APIRouter()


@router.get("/{kit_id}", response_model=KitFullModel, status_code=HTTP_200_OK)
def get_single_kit(*, db: Session = Depends(get_db), kit_id: int):
    kit = crud_kit.get_single(db, kit_id=kit_id)
    if not kit:
        raise HTTPException(status_code=404, detail="Kit not found")

    return kit.as_complete_dict


@router.get("/", response_model=List[KitFullModel], status_code=HTTP_200_OK)
def get_multiple_kits(*, db: Session = Depends(get_db), amount: Optional[int]):
    if not amount: amount = 10
    if not 0 < amount <= 200: raise HTTPException(HTTP_400_BAD_REQUEST, "Amount should be between the range 1 to 200")
    return [k.as_complete_dict for k in crud_kit.get_multi(db, amount=amount)]


@router.post("/", response_model=KitFullModel, status_code=HTTP_201_CREATED)
def create_single_kit(*, db: Session = Depends(get_db), serial: str, response: Response, body: Optional[KitUpdate]):
    kit, created = crud_kit.create_single(db, serial=serial)

    if not created:
        response.status_code = HTTP_200_OK

    if body: update_kit(kit, body)
    return kit.as_complete_dict


@router.put("/", response_model=KitFullModel, status_code=HTTP_200_OK)
def update_single_kit(*, db: Session = Depends(get_db), kit_id: int, body: KitUpdate):
    kit = crud_kit.get_single(db, kit_id=kit_id)

    if not kit:
        raise HTTPException(status_code=404, detail="Kit not found")

    return update_kit(kit, body).as_complete_dict


def update_kit(kit: KitInDB, body: KitUpdate):
    if body.longitude and body.latitude:
        kit.set_location(body.longitude, body.latitude)

    return kit
