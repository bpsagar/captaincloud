import six
from .meta import TaskMeta
from .registry import TaskRegistry


@six.add_metaclass(TaskMeta)
class Task(object):
    """Base class for tasks"""

    def __new__(cls, **kwargs):
        """Instantiate and set fieldsets"""
        instance = super(Task, cls).__new__(cls)
        for name, fieldset in cls.__fieldsets__.items():
            setattr(instance, name, fieldset())
        return instance

    def __init__(self, **kwargs):
        """Initialize all input fields"""
        self.set_input(**kwargs)

    def set_input(self, **kwargs):
        """Set values for input fields"""
        for name, value in kwargs.items():
            setattr(self.Input, name, value)

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

    def run(self):
        """Execute the task. Instantiate a TaskImpl instance and pass self
        to give access to input and output fields"""
        task_impl = self.impl(task=self)
        task_impl.run()
