from .base import Field
from .exc import InvalidValueException

import pickle
import six


class ValueField(Field):
    """Base class for value field"""

    def set(self, value):
        raise NotImplementedError

    def get(self, value):
        raise NotImplementedError

    def get_initial(self):
        raise NotImplementedError


class StringField(ValueField):
    """String field class"""

    def __init__(self, default=None, nullable=True):
        super(StringField, self).__init__()
        self._nullable = nullable
        self.default = self.set(value=default)

    def set(self, value):
        if value is None and self._nullable:
            return value
        elif not isinstance(value, six.text_type):
            raise InvalidValueException('Expected a string')
        return value

    def get(self, value):
        return value

    def get_initial(self):
        return self.get(self.default)


class ByteField(ValueField):
    """Byte field class"""

    def __init__(self, default=None, nullable=True):
        super(ByteField, self).__init__()
        self._nullable = nullable
        self.default = self.set(value=default)

    def set(self, value):
        if value is None and self._nullable:
            return value
        elif not isinstance(value, six.binary_type):
            raise InvalidValueException('Expected bytes')
        return value

    def get(self, value):
        return value

    def get_initial(self):
        return self.get(self.default)


class IntegerField(ValueField):
    """Integer field class"""

    def __init__(self, default=None, nullable=True):
        super(IntegerField, self).__init__()
        self._nullable = nullable
        self.default = self.set(value=default)

    def set(self, value):
        if value is None and self._nullable:
            return value
        elif not isinstance(value, int):
            raise InvalidValueException('Expected an integer')
        return value

    def get(self, value):
        return value

    def get_initial(self):
        return self.get(self.default)


class FloatField(ValueField):
    """Float field class"""

    def __init__(self, default=None, nullable=True):
        super(FloatField, self).__init__()
        self._nullable = nullable
        self.default = self.set(value=default)

    def set(self, value):
        if value is None and self._nullable:
            return value
        elif not isinstance(value, float) and not isinstance(value, int):
            raise InvalidValueException('Expected a float')
        return float(value)

    def get(self, value):
        return value

    def get_initial(self):
        return self.get(self.default)


class BooleanField(ValueField):
    """Boolean field class"""

    def __init__(self, default=None, nullable=True):
        super(BooleanField, self).__init__()
        self._nullable = nullable
        self.default = self.set(value=default)

    def set(self, value):
        if value is None and self._nullable:
            return value
        elif not isinstance(value, bool):
            raise InvalidValueException('Expected a boolean')
        return value

    def get(self, value):
        return value

    def get_initial(self):
        return self.get(self.default)


class AnyField(ValueField):
    """Field class for any python type"""

    def __init__(self, default=None):
        super(AnyField, self).__init__()
        self.default = self.set(value=default)

    def set(self, value):
        return value

    def get(self, value):
        return value

    def get_initial(self):
        return self.get(self.default)

    def serialize(self, value):
        return pickle.dumps(value)

    def deserialize(self, value):
        return pickle.loads(value)
