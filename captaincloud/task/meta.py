from .field import Field


class FieldSet(object):
    """Class that contains a list of fields"""

    def __init__(self, *args, **kwargs):
        super(FieldSet, self).__init__(*args, **kwargs)
        self._fields = {}
        for name, field in self.__fields__.items():
            self._fields[name] = field.clone()

    @staticmethod
    def make_field_property(field_name):
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
            new_dct['__fields__'][attr] = field
            new_dct[attr] = cls.make_field_property(field_name=attr)
        return type('FieldSetClass', (cls,), new_dct)


class TaskMeta(type):
    """Meta class for tasks"""

    FIELDSETS = ['Input', 'Output']

    def __new__(mcl, name, bases, dct):
        """Creates a FieldSet class for Input and Output fields"""
        new_dct = dict(dct)
        new_dct['__fieldsets__'] = {}
        for fieldset in TaskMeta.FIELDSETS:
            fieldset_class = new_dct.get(fieldset)
            if not fieldset_class:
                continue
            new_dct['__fieldsets__'][fieldset] = FieldSet.create_class(
                fieldset_class)

        return type.__new__(mcl, name, bases, new_dct)
