from .field import Field


class TaskMeta(type):
    """Meta class for tasks"""

    def __new__(mcl, name, bases, dct):
        """Creates fields as properties for fields in Input and Output class
        in task"""
        new_dct = dict(dct)

        fieldsets = ['Input', 'Output']
        for fieldset in fieldsets:
            FieldSet = new_dct.get(fieldset)
            if not FieldSet:
                continue

            for attr in dir(FieldSet):
                field = getattr(FieldSet, attr)
                if not isinstance(field, Field):
                    continue
                setattr(FieldSet, attr, TaskMeta.make_field_property(field))
            new_dct[fieldset] = FieldSet()

        cls = type.__new__(mcl, name, bases, new_dct)
        return cls

    @staticmethod
    def make_field_property(field):
        """Returns a property function for a field"""

        def _set(self, value):
            field.set(value)

        def _get(self):
            return field.get()

        return property(fget=_get, fset=_set)
