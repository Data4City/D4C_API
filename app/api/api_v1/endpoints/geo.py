from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK
from pygeotile.tile import Tile
from shapely.geometry import box, mapping
from geoalchemy2.shape import from_shape
from sqlalchemy import func
from app.api.utils.db import get_db
from app.db_models.kit import Kit
import json

router = APIRouter()


def as_geojson(geo_tuples):
    features = []
    for id, geo in geo_tuples:
        features.append({
            "type": "Feature",
            "properties": {"kit_id": id},
            "geometry": json.loads(geo)
        }
        )

    return {
        "type": "FeatureCollection",
        "features": features
    }


@router.get("/{z}/{x}/{y}", status_code=HTTP_200_OK)
def get_pois_tilemap(*, db: Session = Depends(get_db), z: float, x: float, y: float):
    try:
        sensor_tile = Tile.from_google(x, y, z)
        nw, se = sensor_tile.bounds
        tile_bounds = box(nw.latitude, se.longitude, se.latitude, nw.longitude)

        tile_bounds = from_shape(tile_bounds)
        geo = db.query(Kit.id, func.ST_AsGeoJson(Kit.geom)).filter(func.ST_Contains(tile_bounds, Kit.geom)).all()

        return as_geojson(geo)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")