import falcon

from sqlalchemy import exists

from models import Kit, Measurement, Value


class ValueResource:
    def on_post(self, req, resp):
        try:
            kit_id = req.get_json('kit_id', dtype=int)
            measurement_id = req.get_json('measurement_id', dtype=int)

            if self.session.query(exists().where(Kit.id == kit_id)).scalar():
                data = req.get_json('data')
                if type(data) is list:
                    for entry in data:
                        v = Value(entry('data'), entry('timestamp'), kit_id, measurement_id)
                        v.save(v, self.session)
            else:
                v = Value(req.get_json('data'), req.get_json('timestamp'), kit_id, measurement_id)
                v.save(v, self.session)

            self.session.commit()

        except falcon.HTTPBadRequest as err:
            resp.status = falcon.HTTP_400
            resp.json = {"error": err.description}
