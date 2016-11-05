from .base import Field


class InvalidValueException(Exception):
    """Exception raised when an invalid value is set"""
    pass


class ValueField(Field):
    """Base class for value field"""

    def set(self, value):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError


class StringField(ValueField):
    """String field class"""

    def __init__(self, default=None):
        super(StringField, self).__init__()
        self._value = None
        if default:
            self.set(value=default)

    def set(self, value):
        if not isinstance(value, str):
            raise InvalidValueException('Expected a string')
        self._value = value

    def get(self):
        return self._value


class IntegerField(ValueField):
    """Integer field class"""

    def __init__(self, default=None):
        super(IntegerField, self).__init__()
        self._value = None
        if default:
            self.set(value=default)

    def set(self, value):
        if not isinstance(value, int):
            raise InvalidValueException('Expected an integer')
        self._value = value

    def get(self):
        return self._value


class FloatField(ValueField):
    """Float field class"""

    def __init__(self, default=None):
        super(FloatField, self).__init__()
        self._value = None
        if default:
            self.set(value=default)

    def set(self, value):
        if not isinstance(value, float) and not isinstance(value, int):
            raise InvalidValueException('Expected a float')
        self._value = float(value)

    def get(self):
        return self._value


class BooleanField(ValueField):
    """Boolean field class"""

    def __init__(self, default=None):
        super(BooleanField, self).__init__()
        self._value = None
        if default is not None:
            self.set(value=default)

    def set(self, value):
        if not isinstance(value, bool):
            raise InvalidValueException('Expected a boolean')
        self._value = value

    def get(self):
        return self._value
