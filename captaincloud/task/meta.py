from .fieldset import FieldSet


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
