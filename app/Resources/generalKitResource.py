import falcon

from Models import Kit


class KitResource:

    def on_get_single(self, req, resp, kit_id=None):
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

    def on_put_single(self, req, res, kit_id):
        kit = self.session.query(Kit).filter_by(Kit.id == kit_id).first()

        if kit:
            if all([el in req.json for el in ["long", "lat"]]):
                kit.set_location(req.get_json("long"), req.get_json("lat"))
        else:
            res.json = {'error': "Kit with given id doesn't exist"}
            res.status = falcon.HTTP_404

    def on_post(self, req, resp):
        try:
            serial = req.get_json("serial", dtype=str)
            kit = self.session.query(Kit).filter(Kit.serial == serial).one_or_none()
            if not kit:
                resp.status = falcon.HTTP_201

                kit = Kit(serial)

                if all([el in req.json for el in ["long", "lat"]]):
                    kit.set_location(req.get_json("long"), req.get_json("lat"))

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
