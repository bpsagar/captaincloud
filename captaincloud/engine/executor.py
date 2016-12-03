from captaincloud.task import Task

import json
import logging
import sys
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
    def __init__(self, workdir='.'):
        self.uuid = str(uuid.uuid4())
        self.logger = logging.getLogger('TaskExecutor')

        self.state = TaskExecutorState.NOT_STARTED
        self.status = TaskExecutorStatus.UNKNOWN

    def set_task(self, task):
        self.task = task
        self.impl = self.task.get_impl()

    def load_task(self, task_in):
        if task_in == 'stdin':
            fd = sys.stdin
        else:
            fd = open(task_in, 'r')
        try:
            task_data = json.load(fd)
            self.task = Task.deserialize(task_data)
            self.impl = self.task.get_impl()
            fd.close()
            return self.task
        except json.decoder.JSONDecodeError:
            fd.close()
            raise Exception('Unable to load task data.')

    def dump_task(self, task_out):
        if task_out == 'stdout':
            fd = sys.stdout
        else:
            fd = open(task_out, 'w')
        json.dump(self.task.serialize(), fd)
        fd.close()

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
