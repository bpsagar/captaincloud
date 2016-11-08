import six
from .meta import TaskMeta
from .registry import TaskRegistry


@six.add_metaclass(TaskMeta)
class Task(object):
    """Base class for tasks"""

    def __new__(cls):
        """Instantiate and set fieldsets"""
        instance = super(Task, cls).__new__(cls)
        for name, fieldset in cls.__fieldsets__.items():
            setattr(instance, name, fieldset())
        return instance

    def serialize(self):
        """Serialize the Task instance"""
        data = {
            'ID': self.ID
        }
        for fieldset in TaskMeta.FIELDSETS:
            fieldset_obj = getattr(self, fieldset)
            data[fieldset] = fieldset_obj.serialize()
        return data

    @classmethod
    def deserialize(cls, data):
        """Deserialize the data into a Task instance"""
        instance = TaskRegistry.get(id=data['ID'])()
        for fieldset in TaskMeta.FIELDSETS:
            fields = data[fieldset]
            FieldSet = getattr(instance, fieldset)
            for field, value in fields.items():
                setattr(FieldSet, field, value)
        return instance
