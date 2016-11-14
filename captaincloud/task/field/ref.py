from .base import Field
from .exc import InvalidValueException


class ReferenceField(Field):
    pass


class ListValue(list):
    def __init__(self, ref_type):
        super(ListValue, self).__init__()
        self.ref_type = ref_type

    def append(self, item):
        self.ref_type.set(item)
        super(ListValue, self).append(self.ref_type.get())


class ListField(ReferenceField):
    def __init__(self, ref_type, default=[]):
        super(ListField, self).__init__()
        self.ref_type = ref_type
        self.items = ListValue(ref_type=ref_type)

        for item in default:
            self.append(item)

    def get(self):
        return self.items

    def set(self, value):
        try:
            iterable = iter(value)
        except TypeError:
            raise InvalidValueException('Expected iterable')
        self.clear()
        for item in iterable:
            self.append(item)

    def clear(self):
        self.items = ListValue(ref_type=self.ref_type)

    def append(self, item):
        self.items.append(item)

    def pop(self, pos=-1):
        return self.items.pop(pos)

    def clone(self):
        clone = self.__class__(ref_type=self.ref_type)
        clone.set(self.get())
        return clone

    def serialize(self, value):
        result = []
        for item in value:
            result.append(self.ref_type.serialize(item))
        return result

    def deserialize(self, value):
        result = []
        for item in value:
            result.append(self.ref_type.deserialize(item))
        return result
