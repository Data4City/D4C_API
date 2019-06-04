import falcon
from pygeotile.tile import Tile
from shapely.geometry import box, mapping
from geoalchemy2.shape import from_shape
from sqlalchemy import func

from Models import Kit

import json
class GeoResource:
    @classmethod
    def as_geojson(self, geo_tuples):
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

    def on_get(self, req, resp, z, x, y):
        try:
            sensor_tile = Tile.from_google(x, y, z)
            nw, se = sensor_tile.bounds
            tile_bounds = box(nw.latitude, se.longitude, se.latitude, nw.longitude)

            tile_bounds = from_shape(tile_bounds)
            geo = self.session.query(Kit.id, func.ST_AsGeoJson(Kit.geom)).filter(func.ST_Contains(tile_bounds,Kit.geom)).all()

            resp.json = self.as_geojson(geo)
            resp.status = falcon.HTTP_200
        except Exception:
            resp.status = falcon.HTTP_500