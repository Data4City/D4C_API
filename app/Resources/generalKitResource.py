import falcon
from sqlalchemy import exists

from models import Kit


class KitResource:
    def create_kit(self, serial):
        b = Kit(serial)
        b.save(self.session)
        return b

    def on_post(self, req, resp):
        try:
            serial = req.get_json("serial", dtype=str)
            kit = self.session.query(Kit).filter(Kit.serial == serial).first()
            if kit:
                resp.status = falcon.HTTP_200
                resp.json = kit.as_simple_dict
            else:
                self.create_kit(kit)
                resp.status = falcon.HTTP_401
                resp.json = kit.as_simple_dict
        except falcon.HTTPBadRequest:
            resp.json = {'error': "Field 'serial' is required"}


class GeneralKitResource:
    def on_get(self, req, resp, kit_id):
        try:
            kit = self.session.query(Kit).get(kit_id)
            if kit is not None:
                resp.status = falcon.HTTP_200
                resp.json = kit.as_complete_dict
            else:
                resp.status = falcon.HTTP_404
                resp.json = {'error': "Kit with id {} doesn't exist".format(kit_id)}
        except falcon.HTTPBadRequest as e:
            resp.json = {'error': "Field 'id' is required"}
