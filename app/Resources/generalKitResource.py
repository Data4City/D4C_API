import falcon

from Helpers.helper_functions import get_or_create
from sqlalchemy.sql import exists
from models import Kit


class KitResource:

    def on_post(self, req, resp):
        try:
            serial = req.get_json("serial", dtype=str)
            kit = self.session.query(Kit).filter(Kit.serial == serial).one_or_none()
            if not kit:
                resp.status = falcon.HTTP_201

                if all([el in req.json for el in ["long", "lat"]]):
                    kit = Kit(serial)
                    kit.set_location(req.get_json("lat"), req.get_json("long"))
                    kit.save(self.session)

                else:
                    kit = Kit(serial)
                    kit.save(self.session)
            else:
                resp.status = falcon.HTTP_200

            resp.json = kit.as_simple_dict
        except falcon.HTTPBadRequest:
            resp.json = {'error': "Field 'serial' is required"}

    def on_get(self, req, resp):
        amount = 10
        try:
            amount = int(req.params.get("amount", 10))
        except ValueError:
            amount = amount

        results = self.session.query(Kit).limit(amount).all()
        resp.json = [k.as_simple_dict for k in results]
        resp.status = falcon.HTTP_200


class GeneralKitResource:
    def on_get(self, req, resp, kit_id):
        try:
            kit = self.session.query(Kit).get(kit_id)
            if kit:
                resp.status = falcon.HTTP_200
                resp.json = kit.as_complete_dict
            else:
                resp.status = falcon.HTTP_404
                resp.json = {'error': "Kit with id {} doesn't exist".format(kit_id)}
        except falcon.HTTPBadRequest as e:
            resp.json = {'error': "Field 'id' is required"}
