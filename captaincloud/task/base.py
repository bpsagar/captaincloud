from .registry import TaskRegistry
from .field import StructField

"""
Task is the base class for defining metadata for the task to be performed.
Derived class must define 2 sub classes, Input and Output, within which input
and output fields can be defined respectively.
Attributes that derive from the Field class are considered to be vaild fields,
and rest of them will just be ignored.
Input and Output are replaced with the StructField, at runtime, as they denote
structural information.
ID attribute must be specified while working with TaskRegsitry.
impl attribute must be specified with Implementation class for the task. Note
that implementation class must be a derived class of TaskImpl.
"""


class Task(object):
    """Base class for tasks"""

    FIELDSETS = ['Input', 'Output']

    def __new__(cls, **kwargs):
        """Instantiate and set fieldsets"""
        instance = super(Task, cls).__new__(cls)
        # For each FIELDSET (Input and Output), create Struct Field based on
        # the definition.
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
        """Convert task object into serializable dictionary object"""
        data = {
            'ID': self.ID
        }
        for fieldset in self.FIELDSETS:
            fieldset_obj = getattr(self, fieldset)
            data[fieldset] = fieldset_obj.serialize()
        return data

    @classmethod
    def deserialize(cls, data):
        """Restore task object from deserialized dictionary object"""
        instance = TaskRegistry.get(id=data['ID'])()
        for fieldset in cls.FIELDSETS:
            fields = data[fieldset]
            fieldset_obj = getattr(instance, fieldset)
            setattr(instance, fieldset, fieldset_obj.deserialize(fields))
        return instance

    def get_impl(self):
        """Create instance of the implementation class"""
        return self.impl(task=self)

    def run(self, logger=None):
        """Execute the task. Instantiate a TaskImpl instance and pass self
        to give access to input and output fields"""
        task_impl = self.impl(task=self, logger=logger)
        task_impl.run()
