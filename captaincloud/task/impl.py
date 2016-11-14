import logging


class TaskImpl(object):
    """Base class for task implementation"""

    def __init__(self, task, logger=None):
        super(TaskImpl, self).__init__()
        self.task = task
        if logger is None:
            self.logger = logging.getLogger(self.__class__.__name__)
        else:
            self.logger = logger

    def run(self):
        """Execute the task, needs to be implemented by derived classes"""
        raise NotImplementedError
