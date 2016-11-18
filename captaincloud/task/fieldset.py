from .field import Field, StreamField, ValueField, ReferenceField


class FieldSet(object):
    """Class that contains a list of fields"""

    def __init__(self, *args, **kwargs):
        super(FieldSet, self).__init__(*args, **kwargs)
        self._field_values = {}
        for name, field in self.__fields__.items():
            self._field_values[name] = field.get_initial()

    @classmethod
    def create_class(cls, fieldset_class):
        """Create a fieldset class"""
        new_dct = dict(cls.__dict__)
        new_dct['__fields__'] = {}

        for attr in dir(fieldset_class):
            field = getattr(fieldset_class, attr)
            if not isinstance(field, Field):
                continue
            new_dct['__fields__'][attr] = field
            new_dct[attr] = field.make_property(attr)
        return type('FieldSetClass', (cls,), new_dct)

    def serialize(self):
        """Serialize fieldset"""
        data = {}
        for field in self._field_values:
            field_type = self.__fields__[field]
            if field_type.is_serializable():
                data[field] = field_type.serialize(getattr(self, field))
        return data

    def deserialize(self, data):
        for field, value in data.items():
            if field in self.__fields__:
                field_type = self.__fields__.get(field)
            setattr(self, field, field_type.deserialize(value))
