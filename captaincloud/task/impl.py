
class TaskImpl(object):
    """Base class for task implementation"""

    def __init__(self, task):
        super(TaskImpl, self).__init__()
        self.task = task

    def run(self):
        """Execute the task, needs to be implemented by derived classes"""
        raise NotImplementedError
