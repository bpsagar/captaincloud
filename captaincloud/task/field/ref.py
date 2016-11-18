from .base import Field
from .exc import InvalidValueException


class ReferenceField(Field):
    pass


class ListValue(list):
    def __init__(self, ref_type):
        super(ListValue, self).__init__()
        self.ref_type = ref_type

    def append(self, item):
        super(ListValue, self).append(self.ref_type.set(item))


class ListField(ReferenceField):
    def __init__(self, ref_type, default=[]):
        super(ListField, self).__init__()
        self.ref_type = ref_type
        self.default = default

    def get(self, value):
        return value

    def set(self, value):
        val = ListValue(ref_type=self.ref_type)
        for item in value:
            val.append(item)
        return val

    def create(self):
        val = ListValue(ref_type=self.ref_type)
        for item in self.default:
            val.append(item)
        return val

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


class ComplexField(ReferenceField):
    pass
