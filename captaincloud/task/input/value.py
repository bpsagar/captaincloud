from ..mixin import FloatMixin, IntegerMixin, StringMixin
from .base import Input


class ValueInput(Input):
    """Base class for value input"""

    def set(self, value):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError


class StringInput(StringMixin, ValueInput):
    """String input class"""

    def __init__(self, default=None):
        super(StringInput, self).__init__()
        self._value = None
        if default:
            self.set(value=default)


class IntegerInput(IntegerMixin, ValueInput):
    """Integer input class"""

    def __init__(self, default=None):
        super(IntegerInput, self).__init__()
        self._value = None
        if default:
            self.set(value=default)


class FloatInput(FloatMixin, ValueInput):
    """Float input class"""

    def __init__(self, default=None):
        super(FloatInput, self).__init__()
        self._value = None
        if default:
            self.set(value=default)
