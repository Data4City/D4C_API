import falcon

from Helpers.helper_functions import get_or_create
from Models import Kit, Sensor


class SensorResource:
    def create_sensor(self, req):
        name = req.get_json('name', dtype=str, max=40)
        model = req.get_json('model', dtype=str, max=40)

        return get_or_create(self.session, Sensor, name=name, model=model)

    def on_post(self, req, resp):
        try:
            sensor, s_created = self.create_sensor(req)
            resp.status = falcon.HTTP_201 if s_created else falcon.HTTP_200
            resp.json = sensor.as_dict

        except falcon.HTTPBadRequest as err:
            resp.status = falcon.HTTP_400
            resp.json = {'error': err.description}

    def on_post(self, req, resp, kit_id):
        try:

            kit, k_created = get_or_create(self.session, Kit, id=kit_id)
            sensor, s_created = self.create_sensor(req)

            if k_created or s_created:
                sensor.add_kit(kit, self.session)
            resp.json = sensor.as_dict
            resp.status = falcon.HTTP_201

        except falcon.HTTPBadRequest as err:
            resp.status = falcon.HTTP_400
            resp.json = {'error': err.description}
