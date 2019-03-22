import models
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
        self.assertEqual({'error': "Box already exists"}, result.json)

    def test_02_sensor_post(self):
        create_body = {'kit_id': 1, 'name': "Fake sensor", 'model': "Fakerino"}
        assert_dict = {'id': 1, 'name': "Fake sensor", 'model': "Fakerino", 'measurements': []}
        route = '/v1/sensor'
        result = self.simulate_post(route, json=create_body)
        self.assertEqual(assert_dict, result.json)
        self.assertEqual(result.status, falcon.HTTP_201)

    def test_03_sensor_put_measurement(self):
        route = '/v1/sensor'
        measurement_create = {"sensor_id": 1, "symbol": "m", "name": "meters"}
        assert_dict = {'id': 1, 'name': "Fake sensor", 'model': "Fakerino", 'measurements': [{'name': 'meters', 'symbol': 'm'}],}

        result = self.simulate_put(route, json=measurement_create)

        self.assertEqual(assert_dict, result.json)

    def test_04_kit_get(self):
        route = '/v1/kit'

        assert_dict = {'id': 1,
                       'sensors_used': [
                           {'id': 1, 'model': 'Fakerino', 'name': 'Fake sensor',
                            'measurements': [{'name': 'meters', 'symbol': 'm'}],}
                       ],
                       'serial': 'E00R000050600000'}

        # Error because no response
        result = self.simulate_get(route)
        self.assertEqual({'error': "Field 'id' is required"}, result.json)

        # Error because id that doesn't exist
        result = self.simulate_get(route, json={'id': 2})
        self.assertEqual({'error': "Box with id 2 doesn't exist"}, result.json)

        result = self.simulate_get(route, json={'id': 1})
        result_jay = result.json
        result_jay.pop('created_at')
        self.assertEqual(assert_dict, result_jay)


if __name__ == '__main__':
    unittest.main()
