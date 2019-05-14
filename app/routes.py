from Resources import *


def add_routes(_app):
    _app.add_route('/v1/kit', KitResource())
    _app.add_route('/v1/{kit_id:int}/kit', GeneralKitResource())
    _app.add_route('/v1/{kit_id:int}/sensor', SensorResource())
    _app.add_route('/v1/measurement/{sensor_id:int}', MeasurementResource())
    _app.add_route('/v1/{kit_id:int}/{measurement_id:int}/values', ValueResource())
    _app.add_route('/debug', DebugResource())
