from datetime import datetime

import falcon
from sqlalchemy import exists

from Models import Kit, Value


class ValueResource:
    def process_entry(self, entry, kit_id, measurement_id):
        if all([key in entry for key in ["data", "timestamp"]]):
            date = datetime.strptime(entry['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            v = Value(entry['data'], date, kit_id, measurement_id)
            v.save(self.session)
        else:
            raise falcon.HTTPBadRequest

    def on_post(self, req, resp, kit_id, measurement_id):
        try:
            if self.session.query(exists().where(Kit.id == kit_id)).scalar():
                data = req.get_json("data")
                if type(data) is list:
                    for entry in data:
                        self.process_entry(entry, kit_id, measurement_id)
                else:
                    self.process_entry(data, kit_id, measurement_id)
                self.session.commit()

            resp.status = falcon.HTTP_201
            resp.json = {"OK": "Saved successfully"}
        except falcon.HTTPBadRequest as err:
            resp.status = falcon.HTTP_400
            resp.json = {"error": err.description}
