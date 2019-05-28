from Resources import *


def add_routes(_app):
    from Helpers.converters import FloatConverter

    _app.router_options.converters['float'] = FloatConverter

    _app.add_route('/v1/kit', KitResource())
    _app.add_route('/v1/kit/{kit_id:int}', KitResource(), suffix="single")
    _app.add_route('/v1/kit/{kit_id:int}/sensor', SensorResource())
    _app.add_route('/v1/kit/{kit_id:int}/measurement/{measurement_id:int}', ValueResource())

    _app.add_route('/v1/sensor/', SensorResource())
    _app.add_route('/v1/sensor/{sensor_id:int}/measurement', MeasurementResource())

    _app.add_route('/v1/geo/{z:float}/{x:float}/{y:float}', GeoResource())

    _app.add_route('/debug', DebugResource())
