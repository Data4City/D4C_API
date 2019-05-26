from falcon.routing import BaseConverter


class FloatConverter(BaseConverter):
    def convert(self, value):
        try:
            return float(value)
        except ValueError:
            return None


