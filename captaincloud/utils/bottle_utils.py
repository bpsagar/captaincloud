import json
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
