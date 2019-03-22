import falcon

from Helpers.custom_decorators import validate, get_json_body
from Helpers.helper_functions import get_or_create
from models import *


class SensorResource(object):

    #        measurement_create = {"symbol": "m", "name": "meters"}

    def on_put(self, req, resp):
        try:
            sensor_id = req.get_json('sensor_id', dtype=int)

            sensor = get_or_create(self.session, Sensor, id=sensor_id)

            symbol = req.get_json('symbol', dtype=str, max=40)
            name = req.get_json('name', dtype=str, max=40)

            measurement = get_or_create(self.session, Measurement, symbol=symbol, name=name)
            measurement.add_sensor(sensor, self.session)

            resp.media = sensor.as_dict
            resp.status = falcon.HTTP_201

        except falcon.HTTPBadRequest as err:
            resp.status = falcon.HTTP_400
            resp.media = {'error': err.description}

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

        except falcon.HTTPBadRequest as err:
            resp.status = falcon.HTTP_400
            resp.body = {'error': err.description}
