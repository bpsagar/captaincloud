
IS_API_ATTR = '_API'


def register(fn):
    """Decorator method to register as API view"""
    setattr(fn, IS_API_ATTR, True)
    return fn


def get_methods(instance):
    """Returns a list of method names that are registers as API"""
    methods = []
    for attr in dir(instance):
        value = getattr(instance, attr)
        if hasattr(value, IS_API_ATTR):
            methods.append(attr)
    return methods
