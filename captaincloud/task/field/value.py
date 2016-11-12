from .base import Field
from .exc import InvalidValueException

import six


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
        if default is not None:
            self.set(value=default)

    def set(self, value):
        if not isinstance(value, six.text_type):
            raise InvalidValueException('Expected a string')
        self._value = value

    def get(self):
        return self._value


class ByteField(ValueField):
    """Byte field class"""

    def __init__(self, default=None):
        super(ByteField, self).__init__()
        self._value = None
        if default is not None:
            self.set(value=default)

    def set(self, value):
        if not isinstance(value, six.binary_type):
            raise InvalidValueException('Expected bytes')
        self._value = value

    def get(self):
        return self._value


class IntegerField(ValueField):
    """Integer field class"""

    def __init__(self, default=None):
        super(IntegerField, self).__init__()
        self._value = None
        if default is not None:
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
        if default is not None:
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


class ListField(ValueField):
    """List field class"""

    def __init__(self, type, default=None):
        super(ListField, self).__init__()
        self._type = type
        self._value = []
        if default is not None:
            self.set(value=default)

    def set(self, value):
        if not isinstance(value, list):
            raise InvalidValueException('Expected a list')
        self._value = []
        for item in value:
            self.append(item)

    def get(self):
        return [item.get() for item in self._value]

    def append(self, item):
        """Add an item to the list"""
        item_obj = self._type(default=item)
        self._value.append(item_obj)

    def pop(self, *args, **kwargs):
        """Pop a value from the list"""
        value = self._value.pop(*args, **kwargs)
        return value.get()
