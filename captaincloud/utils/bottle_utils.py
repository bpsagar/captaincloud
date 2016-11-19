import json
import requests
from bottle import Bottle, request

IS_API_ATTR = '_API'


def register_api(fn):
    """Decorator method to register as API view"""
    setattr(fn, IS_API_ATTR, True)
    return fn


def get_api_methods(instance):
    """Returns a list of method names that are registers as API"""
    methods = []
    for attr in dir(instance):
        value = getattr(instance, attr)
        if hasattr(value, IS_API_ATTR):
            methods.append(attr)
    return methods


def view_wrapper(fn):
    """Bottle view wrapper"""
    def _inner():
        kwargs = json.loads(request.forms.get('data'))
        try:
            response = {
                'data': fn(**kwargs),
                'status': 'OK'
            }
        except:
            response = {'status': 'ERROR', 'data': {}}
        return response
    return _inner


def make_app(instance, mount):
    """Make a bottle app from the instance"""
    sub_app = Bottle()
    for method_name in get_api_methods(instance):
        method = getattr(instance, method_name)
        route = '/%s/' % method_name
        sub_app.route(route, method='POST')(view_wrapper(method))

    app = Bottle()
    app.mount(mount, sub_app)
    return app


def client_method(url):
    """Returns a method that accepts keyword arguments and posts to url and
    returns the JSON response as a dictionary"""
    def _inner(**kwargs):
        data = json.dumps(kwargs)
        response = requests.post(url, {'data': data})
        return response.json().get('data', {})
    return _inner


class Client(object):
    """Generic client for an HTTP application. Used to access APIs as local
    method calls."""

    def __init__(self, base_url, methods):
        self._base_url = base_url
        self._methods = methods

    def __getattr__(self, name):
        """Returns the client_method if the name of the attribute is one of the
        API methods"""
        if name not in self._methods:
            raise AttributeError
        url = '%s/%s/' % (self._base_url, name)
        return client_method(url=url)


def make_client(instance, base_url):
    """Make a client for the instance and base_url"""
    return Client(base_url=base_url, methods=get_api_methods(instance))
