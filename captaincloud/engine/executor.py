import logging
import uuid


class TaskExecutorState(object):
    NOT_STARTED = 'NOT_STARTED'
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'


class TaskExecutorStatus(object):
    UNKNOWN = 'UNKNOWN'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'


class TaskExecutor(object):
    def __init__(self, task, context=None, settings=None):
        self.task = task
        self.impl = task.get_impl()
        self.context = context or dict()
        self.settings = settings or dict()

        self.uuid = str(uuid.uuid4())
        self.logger = logging.getLogger('TaskExecutor')

        self.state = TaskExecutorState.NOT_STARTED
        self.status = TaskExecutorStatus.UNKNOWN

    def execute(self):
        """Execute the task"""
        try:
            self.state = TaskExecutorState.RUNNING
            self.run()
            self.status = TaskExecutorStatus.SUCCESS
        except Exception:
            self.status = TaskExecutorStatus.FAILURE
        self.state = TaskExecutorState.COMPLETED

    def run(self):
        self.impl.run()
