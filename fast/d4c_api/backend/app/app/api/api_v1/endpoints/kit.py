# def on_get_single(self, req, resp, kit_id=None):
#     try:
#         kit = self.session.query(Kit).get(kit_id)
#         if kit:
#             resp.status = falcon.HTTP_200
#             resp.json = kit.as_complete_dict
#         else:
#             resp.status = falcon.HTTP_404
#             resp.json = {'error': "Kit with id {} doesn't exist".format(kit_id)}
#     except falcon.HTTPBadRequest as e:
#         resp.json = {'error': "Field 'id' is required"}
from typing import List
from sqlalchemy.orm import Session
from app import crud

from app.api.utils.db import get_db
from app.models.kit import KitModel
from fastapi import APIRouter, Body, Depends, HTTPException


router = APIRouter()


@router.get("/", response_model=KitModel)
def get_single_kit(*,db: Session = Depends(get_db), kit_id: int ):
    return crud.kit.get(db, kit_id=kit_id)
