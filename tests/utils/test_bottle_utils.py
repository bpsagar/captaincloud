import json
import time
import unittest
from multiprocessing import Process
from webtest import TestApp
from captaincloud.utils import bottle_utils


class TestBottleUtils(unittest.TestCase):
    """Tests for bottle utils"""

    def setUp(self):
        class Test1:
            @bottle_utils.register_api
            def endpoint1(self):
                pass

            @bottle_utils.register_api
            def endpoint2(self):
                pass

        class Test2:
            def __init__(self, value):
                self.value = value

            @bottle_utils.register_api
            def endpoint(self, arg1):
                if arg1 == 'error':
                    raise Exception('Dummy exception')
                return {'works': True, 'arg1': arg1, 'value': self.value}

        self.Test1 = Test1
        self.Test2 = Test2

    def test_register_api(self):

        @bottle_utils.register_api
        def dummy():
            pass

        self.assertTrue(hasattr(dummy, bottle_utils.IS_API_ATTR))
        self.assertTrue(getattr(dummy, bottle_utils.IS_API_ATTR))
        dummy()  # For 100% coverage :D

    def test_get_api_methods(self):
        test = self.Test1()
        methods = bottle_utils.get_api_methods(instance=test)
        self.assertEqual(methods, ['endpoint1', 'endpoint2'])

        # For 100% coverage :D
        test.endpoint1()
        test.endpoint2()

    def test_make_app(self):
        test = self.Test2(value=10)
        app = bottle_utils.make_app(instance=test, mount='/api')
        test_app = TestApp(app)

        params = {'arg1': 'test'}
        response = test_app.post(
            '/api/endpoint/', {'data': json.dumps(params)})
        expected_response = {
            'data': {'works': True, 'arg1': 'test', 'value': 10},
            'status': 'OK'
        }
        self.assertEqual(response.json, expected_response)

        params = {'arg1': 'error'}
        response = test_app.post(
            '/api/endpoint/', {'data': json.dumps(params)})
        expected_response = {
            'data': {},
            'status': 'ERROR'
        }
        self.assertEqual(response.json, expected_response)

    def test_make_client(self):
        test = self.Test2(value=10)
        app = bottle_utils.make_app(instance=test, mount='/api')
        process = Process(
            target=app.run, kwargs={'host': 'localhost', 'port': 10000})
        process.start()

        time.sleep(1)  # Wait for the app to run

        client = bottle_utils.make_client(
            instance=test, base_url='http://localhost:10000/api')
        data = client.endpoint(arg1='test')
        expected_data = {'works': True, 'arg1': 'test', 'value': 10}
        self.assertEqual(data, expected_data)

        with self.assertRaises(AttributeError):
            client.invalid_endpoint()

        test.endpoint(arg1='test')  # For 100% coverage :D

        app.close()
        process.terminate()
