import falcon

from app.Helpers.helper_functions import get_or_create
from app.models import Kit, Sensor


class SensorResource:
    def on_post(self, req, resp):
        try:

            name = req.get_json('name', dtype=str, max=40)
            model = req.get_json('model', dtype=str, max=40)
            kit_id = req.get_json('kit_id', dtype=int)

            sensor = get_or_create(self.session, Sensor, name=name, model=model)
            kit = get_or_create(self.session, Kit, id=kit_id)

            sensor.add_kit(kit, self.session)
            resp.json = sensor.as_dict
            resp.status = falcon.HTTP_201

        except falcon.HTTPBadRequest as err:
            resp.status = falcon.HTTP_400
            resp.json = {'error': err.description}
