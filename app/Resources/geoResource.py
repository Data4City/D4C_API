from pygeotile.tile import Tile
from shapely.geometry import box
from geoalchemy2.shape import from_shape

from Models import Kit


class GeoResource:
    @classmethod
    def as_geojson(self, kits):
        features = []
        for kit in kits:
            features.append({
                "type": "Feature",
                "properties": kit.as_simple_dict,
                "geometry": {
                    "type": "Point",
                    "coordinates": kit.get_position()
                }
            })
        return {
            "type": "FeatureCollection",
            "features": features
        }

    def on_get(self, req, resp, z, x, y):
        sensor_tile = Tile.from_google(x, y, z)
        nw, se = sensor_tile.bounds
        tile_bounds = from_shape(box(nw.longitude, se.latitude, se.longitude, nw.latitude))
        print(tile_bounds)
        kits = self.session.query(Kit).filter(
            tile_bounds.ST_INTERSECTS(Kit.geom))
        print(kits.query(func.count(Kit.id)))
        resp.json = self.as_geojson(kits)
