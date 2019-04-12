import falcon
from sqlalchemy import exists

from app.models import Kit


class KitResource:
    def create_kit(self, serial):
        b = Kit(serial)
        b.save(self.session)
        return b

    def on_get(self, req, resp):
        try:
            kit_id = req.get_json('id', dtype=int)
            kit = self.session.query(Kit).get(kit_id)
            if kit is not None:
                response = kit.as_dict
                resp.status = falcon.HTTP_200
                resp.json = response
            else:
                resp.status = falcon.HTTP_404
                resp.json = {'error': "Kit with id {} doesn't exist".format(kit_id)}
        except falcon.HTTPBadRequest as e:
            try:
                serial = req.get_json("serial", dtype=str)
                kit = self.session.query(Kit).filter(Kit.serial == serial).first()
                if kit:
                    resp.status = falcon.HTTP_200
                    resp.json = kit.as_dict
                else:
                    resp.status = falcon.HTTP_404
                    resp.json = {'error': "Kit with serial {} doesn't exist".format(serial)}
            except falcon.HTTPBadRequest as e:
                resp.status = falcon.HTTP_400
                resp.json = {'error': "Field 'serial' or 'id' is required"}

    def on_post(self, req, resp):
        try:
            serial = req.get_json('serial', dtype=str, max=16)
            # If kit already exists
            if not self.session.query(exists().where(Kit.serial == serial)).scalar():
                b = self.create_kit(serial)
                resp.json = b.as_dict
                resp.status = falcon.HTTP_201
            else:
                resp.status = falcon.HTTP_403
                resp.json = {"error": "Kit already exists"}
        except falcon.HTTPBadRequest as err:
            resp.status = falcon.HTTP_400
            resp.json = {"error": err.description}
        except Exception as err:
            resp.status = falcon.HTTP_400
            resp.json = {"error": err.description}
