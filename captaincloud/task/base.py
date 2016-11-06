import six
from .meta import TaskMeta


@six.add_metaclass(TaskMeta)
class Task(object):
    """Base class for tasks"""

    def __new__(cls):
        """Instantiate and set fieldsets"""
        instance = super(Task, cls).__new__(cls)
        for name, fieldset in cls.__fieldsets__.items():
            setattr(instance, name, fieldset())
        return instance
