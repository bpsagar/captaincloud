from .field import Field, StreamField, ValueField


class FieldSet(object):
    """Class that contains a list of fields"""

    def __init__(self, *args, **kwargs):
        super(FieldSet, self).__init__(*args, **kwargs)
        self._fields = {}
        for name, field in self.__fields__.items():
            self._fields[name] = field.clone()

    @staticmethod
    def make_value_field_property(field_name):
        """Returns a property function for a field"""

        def _set(self, value):
            self._fields[field_name].set(value)

        def _get(self):
            return self._fields[field_name].get()

        return property(fget=_get, fset=_set)

    @classmethod
    def create_class(cls, fieldset_class):
        """Create a fieldset class"""
        new_dct = dict(cls.__dict__)
        new_dct['__fields__'] = {}
        for attr in dir(fieldset_class):
            field = getattr(fieldset_class, attr)
            if not isinstance(field, Field):
                continue
            if isinstance(field, ValueField):
                new_dct['__fields__'][attr] = field
                new_dct[attr] = cls.make_value_field_property(field_name=attr)
            elif isinstance(field, StreamField):
                pass  # TODO: Implement
        return type('FieldSetClass', (cls,), new_dct)

    def serialize(self):
        """Serialize fieldset"""
        data = {}
        for field in self._fields:
            field_type = self.__fields__.get(field)
            data[field] = field_type.serialize(getattr(self, field))
        return data
