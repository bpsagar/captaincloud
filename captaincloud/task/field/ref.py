from .base import Field


class ReferenceField(Field):
    @classmethod
    def make_property(cls, name):
        def _set(self, value):
            field = self.__fields__.get(name)
            self.__values__[name] = field.create(value)

        def _get(self):
            return self.__values__[name]

        return property(fget=_get, fset=_set)

    @classmethod
    def is_serializable(cls):
        return True

    def create(self, value=None):
        raise NotImplementedError


class ListValue(list):
    def __init__(self, ref_type):
        super(ListValue, self).__init__()
        self.ref_type = ref_type

    def append(self, item):
        self.ref_type.validate(item)
        super(ListValue, self).append(item)


class ListField(ReferenceField):
    def __init__(self, ref_type, default=[]):
        super(ListField, self).__init__()
        self.ref_type = ref_type
        self.default = default

    def get_initial(self):
        return self.create()

    def create(self, value=None):
        val = ListValue(ref_type=self.ref_type)
        for item in (value or self.default):
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


class StructValue(object):
    def __init__(self):
        self.__values__ = {}
        for name, field in self.__fields__.items():
            self.__values__[name] = field.get_initial()

    def serialize(self):
        return self.struct_field.serialize(self)

    @classmethod
    def deserialize(cls, value):
        return cls.struct_field.deserialize(value)


class StructField(ReferenceField):
    def __init__(self, **fields):
        self.__fields__ = {}
        for name, field in fields.items():
            if isinstance(field, Field):
                self.__fields__[name] = field
        self._make_class()

    def _make_class(self):
        new_dct = {}
        new_dct['__fields__'] = {}

        for attr in self.__fields__:
            field = self.__fields__.get(attr)
            new_dct['__fields__'][attr] = field
            new_dct[attr] = field.make_property(attr)
        self.klass = type('StructValueInst', (StructValue,), new_dct)
        self.klass.struct_field = self

    def create(self, value=None):
        return self.klass()

    def get_initial(self):
        return self.create()

    def serialize(self, value):
        result = {}
        for name, field in self.__fields__.items():
            if field.is_serializable():
                result[name] = field.serialize(getattr(value, name))
        return result

    def deserialize(self, value):
        result = self.create()
        for name, field in self.__fields__.items():
            if name in value and field.is_serializable():
                setattr(result, name, field.deserialize(value.get(name)))
        return result
