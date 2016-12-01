import logging

"""
TaskImpl is the base class for Implementation of tasks.
Task metadata is accessible through the member 'task'.
Derived class must implement the run method, where task.Input and Output can be
consumed, as necessary.
run method is free to raise any exception, however, task may be retried and the
implementation should make sure that there are no side effects.
"""


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
