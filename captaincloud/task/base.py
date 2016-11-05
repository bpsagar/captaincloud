import six
from .meta import TaskMeta


@six.add_metaclass(TaskMeta)
class Task(object):
    """Base class for tasks"""
    pass
