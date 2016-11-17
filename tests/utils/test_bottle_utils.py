import json
import unittest
from webtest import TestApp
from captaincloud.utils import bottle_utils


class TestBottleUtils(unittest.TestCase):
    """Tests for bottle utils"""

    def test_register_api(self):

        @bottle_utils.register_api
        def dummy():
            pass

        self.assertTrue(hasattr(dummy, bottle_utils.IS_API_ATTR))
        self.assertTrue(getattr(dummy, bottle_utils.IS_API_ATTR))
        dummy()  # For 100% coverage :D

    def test_get_api_methods(self):

        class Test:
            @bottle_utils.register_api
            def endpoint1(self):
                pass

            @bottle_utils.register_api
            def endpoint2(self):
                pass

        test = Test()
        methods = bottle_utils.get_api_methods(instance=test)
        self.assertEqual(methods, ['endpoint1', 'endpoint2'])

        # For 100% coverage :D
        test.endpoint1()
        test.endpoint2()

    def test_make_app(self):

        class Test:
            @bottle_utils.register_api
            def endpoint(self, arg1):
                if arg1 == 'error':
                    raise Exception('Dummy exception')
                return {'works': True, 'arg1': arg1}

        test = Test()
        app = bottle_utils.make_app(instance=test, mount='/api')
        test_app = TestApp(app)

        params = {'arg1': 'test'}
        response = test_app.post(
            '/api/endpoint/', {'data': json.dumps(params)})
        expected_response = {
            'data': {'works': True, 'arg1': 'test'},
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
