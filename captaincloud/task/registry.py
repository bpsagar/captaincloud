
class TaskRegistry(object):
    """Maintains a registry of tasks available"""

    TASKS = {}  # Registry of tasks

    @classmethod
    def register(cls, new_cls):
        """Register a task"""
        cls.TASKS[new_cls.ID] = new_cls
        return new_cls

    @classmethod
    def all(cls):
        """Returns a dictionary of registered tasks"""
        return list(cls.TASKS.values())

    @classmethod
    def get(cls, id):
        """Returns a specific task class by id"""
        return cls.TASKS.get(id)