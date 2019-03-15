import falcon

from Helpers.custom_decorators import validate, get_json_body
from Helpers.helper_functions import get_or_create
from models import Kit, Sensor


class SensorResource(object):

    def on_put(self, req, resp):
        try:
            serial = req.get_json('serial', dtype=str, max=16)
            sensor_id = req.get_json('sensor.id', dtype=int)
            kit = self.session.query(Kit).get(serial)
            value_list = kit.get_n_from_kit(self.session, serial, req.get_json('amount', dtype=int, min=1))
            resp.status = falcon.HTTP_201
            resp.media = {'kit': kit.as_dict(), 'values': [value.as_dict for value in value_list]}

        except Exception as err:
            resp.status = falcon.HTTP_400
            resp.body = {'error': err.description}

    def on_post(self, req, resp):
        try:
            name = req.get_json('name', dtype=str, max=40)
            model = req.get_json('model', dtype=str, max=40)
            kit_id = req.get_json('kit_id', dtype=int)
            sensor = get_or_create(self.session, Sensor, name=name, model=model)
            kit = get_or_create(self.session, Kit, id=kit_id)
            sensor.add_kit(kit, self.session)
            resp.media = sensor.as_dict
            resp.status = falcon.HTTP_201
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.body = {'error': "Bad Request"}
