import falcon

from Helpers.helper_functions import get_or_create, filter_request
from models import Measurement, Sensor


class MeasurementResource:
    def on_post(self, req, resp):
        try:
            sensor_id = req.get_json('sensor_id', dtype=int)

            sensor = get_or_create(self.session, Sensor, id=sensor_id)

            symbol = req.get_json('symbol', dtype=str, max=10)
            name = req.get_json('name', dtype=str, max=30)

            measurement = get_or_create(self.session, Measurement, symbol=symbol, name=name)
            measurement.add_sensor(sensor, self.session)
            resp.status = falcon.HTTP_201
            resp.json = sensor.as_dict

        except falcon.HTTPBadRequest as err:
            resp.status = falcon.HTTP_400
            resp.json = {'error': err.description}

    def on_put(self, req, resp):
        try:
            measurement_id = req.get_json('measurement_id', dtype=int)

            filtered_req = filter_request(Measurement, req.json)
            if filtered_req:
                self.session.query(Measurement).filter(Measurement.id == measurement_id).update(filtered_req)

                resp.json = {"success": "Measurement with id {} updated successfully".format(measurement_id)}
                resp.status = falcon.HTTP_201
            else:
                resp.json = {"error": "empty request"}
                resp.status = falcon.HTTP_400
        except falcon.HTTPBadRequest as err:
            resp.status = falcon.HTTP_400
            resp.json = {'error': err.description}