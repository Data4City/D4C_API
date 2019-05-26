from pygeotile.tile import Tile
from shapely.geometry import box, mapping
from geoalchemy2.shape import from_shape
from sqlalchemy import func

from Models import Kit

import json
class GeoResource:
    @classmethod
    def as_geojson(self, mother):
        features = []
        for id, geo in mother:
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
        sensor_tile = Tile.from_google(x, y, z)
        print(sensor_tile)
        nw, se = sensor_tile.bounds
        tile_bounds = box(nw.latitude, se.longitude, se.latitude, nw.longitude)

        print(mapping(tile_bounds))
        tile_bounds = from_shape(tile_bounds)
        print(nw)
        print(se)
        geo = self.session.query(Kit.id, Kit.geom).filter(
            Kit.geom.ST_Intersects(tile_bounds))
        # print(kits.query(func.count(Kit.id)))
        ass = self.session.query(Kit.id, Kit.geom).filter(
            func.ST_Contains(Kit.geom, tile_bounds)
        )
        print(geo)
        print(geo.all())
        print(ass)
        print(ass.all())

      #  ks= self.session.query(Kit.id,func.ST_AsGeoJSON(Kit.geom)).filter(func.ST_Distance_Sphere(Kit.geom, tile_bounds) < 500000000).all()
       # resp.json = self.as_geojson(ks)
