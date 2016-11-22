import json
from bottle import Bottle, request
from .api import get_methods


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


def make_app(*apps):
    """Make a bottle app from the instance"""
    app = Bottle()

    for mount, instance in apps:
        sub_app = Bottle()
        for method_name in get_methods(instance):
            method = getattr(instance, method_name)
            route = '/%s/' % method_name
            sub_app.route(route, method='POST')(view_wrapper(method))

        app.mount(mount, sub_app)

    return app
