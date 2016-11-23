import json
import time
import unittest
from threading import Thread
from webtest import TestApp
from wsgiref.simple_server import make_server
from captaincloud.utils.http import api
from captaincloud.utils.http import bottle_api
from captaincloud.utils.http import client


class TestBottleUtils(unittest.TestCase):
    """Tests for bottle utils"""

    class Test1:
        @api.register
        def endpoint1(self):
            pass

        @api.register
        def endpoint2(self):
            pass

    class Test2:
        def __init__(self, value):
            self.value = value

        @api.register
        def endpoint(self, arg1):
            if arg1 == 'error':
                raise Exception('Dummy exception')
            return {'works': True, 'arg1': arg1, 'value': self.value}

    def test_register_api(self):
        @api.register
        def dummy():
            pass

        self.assertTrue(hasattr(dummy, api.IS_API_ATTR))
        self.assertTrue(getattr(dummy, api.IS_API_ATTR))
        dummy()  # For 100% coverage :D

    def test_get_api_methods(self):
        test = self.Test1()
        methods = api.get_methods(instance=test)
        self.assertEqual(methods, ['endpoint1', 'endpoint2'])

        # For 100% coverage :D
        test.endpoint1()
        test.endpoint2()

    def test_make_app(self):
        test = self.Test2(value=10)
        app = bottle_api.make_app(('/api', test))
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
        app = bottle_api.make_app(('/api', test))
        server = make_server('localhost', 10001, app)
        process = Thread(
            target=server.serve_forever)
        process.start()

        time.sleep(1)  # Wait for the app to run

        c = client.make_client(
            instance=test, base_url='http://localhost:10001/api')
        data = c.endpoint(arg1='test')
        expected_data = {'works': True, 'arg1': 'test', 'value': 10}
        self.assertEqual(data, expected_data)

        with self.assertRaises(AttributeError):
            c.invalid_endpoint()

        test.endpoint(arg1='test')  # For 100% coverage :D

        app.close()
        server.shutdown()
        process.join()
