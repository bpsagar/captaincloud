from .base import Field


class ReferenceField(Field):
    @classmethod
    def make_property(cls, name):
        def _set(self, value):
            field = self.__fields__.get(name)
            self._field_values[name] = field.set(value)

        def _get(self):
            field = self.__fields__.get(name)
            return field.get(self._field_values[name])

        return property(fget=_get, fset=_set)

    @classmethod
    def is_serializable(cls):
        return True


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

    def get_initial(self):
        return self.create()

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
