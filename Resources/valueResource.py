from datetime import datetime

import falcon
from sqlalchemy import exists

from models import Kit, Value


class ValueResource:
    def process_entry(self, entry, kit_id):
        if all([key in entry for key in ["data", "timestamp",  "measurement_id"]]):
            date = datetime.strptime(entry['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            v = Value(entry['data'], date, kit_id, entry["measurement_id"])
            v.save(self.session)
        else:
            raise falcon.HTTPBadRequest

    def on_post(self, req, resp):
        # try:
        kit_id = req.get_json("kit_id", dtype=int)
        if self.session.query(exists().where(Kit.id == kit_id)).scalar():
            data = req.get_json("data")
            if type(data) is list:
                for entry in data:
                    self.process_entry(entry, kit_id)
            else:
                self.process_entry(data, kit_id)
            self.session.commit()

        resp.status = falcon.HTTP_201
    # except falcon.HTTPBadRequest as err:
    #     resp.status = falcon.HTTP_400
    #     resp.json = {"error": err.description}
