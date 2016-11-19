import json
import requests
from .api import get_methods


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
    return Client(base_url=base_url, methods=get_methods(instance))
