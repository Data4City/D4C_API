import unittest

import falcon
from falcon import testing

from routes import get_app


class MyTestCase(testing.TestCase):
    def setUp(self):
        super(MyTestCase, self).setUp()
        self.app = get_app()


class TestKitResource(MyTestCase):
    @classmethod
    def setUpClass(cls):
        models.__reset_db__()

    def test_01_kit_post(self):
        route = '/v1/kit'
        create_body = {'serial': "E00R000050600000"}
        assert_dict = {'serial': "E00R000050600000", 'id': 1, 'sensors_used': []}
        result = self.simulate_post(route, json=create_body)
        result_jay = result.json
        result_jay.pop('created_at')
        self.assertEqual(assert_dict, result_jay)

        # Post again to test if it doesnt' create a second one .
        result = self.simulate_post(route, json=create_body)
        self.assertEqual({'error': "Kit already exists"}, result.json)

    def test_02_sensor_post(self):
        create_body = {'kit_id': 1, 'name': "Fake sensor", 'model': "Fakerino"}
        assert_dict = {'id': 1, 'name': "Fake sensor", 'model': "Fakerino", 'measurements': []}
        route = '/v1/sensor'
        result = self.simulate_post(route, json=create_body)
        self.assertEqual(assert_dict, result.json)
        self.assertEqual(result.status, falcon.HTTP_201)

    def test_03_measurement_post(self):
        route = '/v1/measurement'
        measurement_create = {"sensor_id": 1, "symbol": "m", "name": "meters"}
        assert_dict = {'id': 1, 'name': "Fake sensor", 'model': "Fakerino",
                       'measurements': [{'name': 'meters', 'symbol': 'm', 'id': 1}], }

        result = self.simulate_post(route, json=measurement_create)

        self.assertEqual(assert_dict, result.json)

    def test_04_measurement_put(self):
        route = '/v1/measurement'
        measurement_create = {"measurement_id": 1, "symbol": "kP", "name": "kiloPascal"}
        assert_dict = {'success': 'Measurement with id 1 updated successfully'}

        result = self.simulate_put(route, json=measurement_create)

        self.assertEqual(assert_dict, result.json)

        # Test filtering to match model

        req_body = {"measurement_id": 1, "useless": "data", "is": "useless"}
        result = self.simulate_put(route, json=req_body)
        self.assertEqual({"error": "empty request"}, result.json)

    def test_05_kit_get(self):
        route = '/v1/kit'

        assert_dict = {'id': 1,
                       'sensors_used': [
                           {'id': 1, 'model': 'Fakerino', 'name': 'Fake sensor',
                            'measurements': [{'name': 'meters', 'symbol': 'm', "id": 1 },]}
                       ],
                       'serial': 'E00R000050600000'}

        # Error because no response
        result = self.simulate_get(route)

        self.assertEqual({'error': "Field 'serial' or 'id' is required"}, result.json)

        # Error because id that doesn't exist
        result = self.simulate_get(route, json={'id': 2})
        self.assertEqual({'error': "Kit with id 2 doesn't exist"}, result.json)

        result = self.simulate_get(route, json={'id': 1})
        result_jay = result.json
        result_jay.pop('created_at')
        self.assertEqual(assert_dict, result_jay)

        #KIT Get from serial
        result = self.simulate_get(route, json={'serial': 'E00R000050600000'})
        result_jay = result.json
        result_jay.pop('created_at')
        self.assertEqual(assert_dict, result_jay)

    def test_06_value_post(self):
        import datetime
        route = "/v1/i2c"
        date = datetime.datetime.now()
        data = [{"data": i*5, "timestamp": str(date), "measurement_id": 1 } for i in range(5)]
        result = self.simulate_post(route, json={"data":data[0], "kit_id": 1})
        self.assertEqual(result.status, falcon.HTTP_201)

        data = {"data": data, "kit_id": 1}
        result = self.simulate_post(route, json=data)
        self.assertEqual(result.status, falcon.HTTP_201)


if __name__ == '__main__':
    unittest.main()
