
class InvalidValueException(Exception):
    """Exception raised when an invalid value is set"""
    pass


class StringMixin(object):
    """Provides setter and getter methods for string values"""

    def set(self, value):
        if not isinstance(value, str):
            raise InvalidValueException('Expected a string')
        self._value = value

    def get(self):
        return self._value


class IntegerMixin(object):
    """Provides setter and getter methods for integer values"""

    def set(self, value):
        if not isinstance(value, int):
            raise InvalidValueException('Expected an integer')
        self._value = value

    def get(self):
        return self._value


class FloatMixin(object):
    """Provides setter and getter methods for float values"""

    def set(self, value):
        if not isinstance(value, float) and not isinstance(value, int):
            raise InvalidValueException('Expected a float')
        self._value = float(value)

    def get(self):
        return self._value
