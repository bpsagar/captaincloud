from .registry import TaskRegistry
from .field import StructField


class Task(object):
    """Base class for tasks"""

    FIELDSETS = ['Input', 'Output']

    def __new__(cls, **kwargs):
        """Instantiate and set fieldsets"""
        instance = super(Task, cls).__new__(cls)
        for name in cls.FIELDSETS:
            if hasattr(cls, name):
                fields = getattr(cls, name).__dict__
                setattr(instance, name, StructField(**fields).create())
            else:
                setattr(instance, name, StructField().create())

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
        for fieldset in self.FIELDSETS:
            fieldset_obj = getattr(self, fieldset)
            data[fieldset] = fieldset_obj.serialize()
        return data

    @classmethod
    def deserialize(cls, data):
        """Deserialize the data into a Task instance"""
        instance = TaskRegistry.get(id=data['ID'])()
        for fieldset in cls.FIELDSETS:
            fields = data[fieldset]
            fieldset_obj = getattr(instance, fieldset)
            setattr(instance, fieldset, fieldset_obj.deserialize(fields))
        return instance

    def run(self, logger=None):
        """Execute the task. Instantiate a TaskImpl instance and pass self
        to give access to input and output fields"""
        task_impl = self.impl(task=self, logger=logger)
        task_impl.run()
