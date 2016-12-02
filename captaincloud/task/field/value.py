from .base import Field
from .exc import InvalidValueException

import base64
import pickle
import six


class ValueField(Field):
    """Base class for value field"""

    def validate(self, value):
        raise NotImplementedError

    def get_initial(self):
        raise NotImplementedError

    @classmethod
    def is_serializable(cls):
        return True

    @classmethod
    def make_property(cls, name):
        def _set(self, value):
            field = self.__fields__.get(name)
            field.validate(value)
            self.__values__[name] = value

        def _get(self):
            return self.__values__[name]

        return property(fget=_get, fset=_set)


class StringField(ValueField):
    """String field class"""

    def __init__(self, default=None, nullable=True):
        super(StringField, self).__init__()
        self._nullable = nullable
        self.validate(default)
        self.default = default

    def validate(self, value):
        if value is None and self._nullable:
            return
        elif not isinstance(value, six.text_type):
            raise InvalidValueException('Expected a string')

    def get_initial(self):
        return self.default


class ByteField(ValueField):
    """Byte field class"""

    def __init__(self, default=None, nullable=True):
        super(ByteField, self).__init__()
        self._nullable = nullable
        self.validate(default)
        self.default = default

    def validate(self, value):
        if value is None and self._nullable:
            return
        elif not isinstance(value, six.binary_type):
            raise InvalidValueException('Expected bytes')

    def get_initial(self):
        return self.default

    def serialize(self, value):
        pass

    def deserialize(self, value):
        pass


class IntegerField(ValueField):
    """Integer field class"""

    def __init__(self, default=None, nullable=True):
        super(IntegerField, self).__init__()
        self._nullable = nullable
        self.validate(default)
        self.default = default

    def validate(self, value):
        if value is None and self._nullable:
            return
        elif not isinstance(value, int):
            raise InvalidValueException('Expected an integer')

    def get_initial(self):
        return self.default


class FloatField(ValueField):
    """Float field class"""

    def __init__(self, default=None, nullable=True):
        super(FloatField, self).__init__()
        self._nullable = nullable
        self.validate(default)
        self.default = default

    def validate(self, value):
        if value is None and self._nullable:
            return
        elif not isinstance(value, float) and not isinstance(value, int):
            raise InvalidValueException('Expected a float')

    def get_initial(self):
        return self.default


class BooleanField(ValueField):
    """Boolean field class"""

    def __init__(self, default=None, nullable=True):
        super(BooleanField, self).__init__()
        self._nullable = nullable
        self.validate(default)
        self.default = default

    def validate(self, value):
        if value is None and self._nullable:
            return
        elif not isinstance(value, bool):
            raise InvalidValueException('Expected a boolean')

    def get_initial(self):
        return self.default


class AnyField(ValueField):
    """Field class for any python type"""

    def __init__(self, default=None):
        super(AnyField, self).__init__()
        self.validate(default)
        self.default = default

    def validate(self, _):
        pass

    def get_initial(self):
        return self.default

    def serialize(self, value):
        return six.u(base64.b64encode(pickle.dumps(value)))

    def deserialize(self, value):
        return pickle.loads(base64.b64decode(value))
