import logging
import threading
import uuid
from six.moves import queue


class TaskRunner(threading.Thread):
    """Class that has a task queue and runs the tasks one by one"""
    WAITING = 'WAITING'
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'
    ERROR = 'ERROR'

    def __init__(self, *args, **kwargs):
        super(TaskRunner, self).__init__(*args, **kwargs)
        self._queue = queue.Queue()
        self._is_running = False
        self._tasks = {}

    def get_task(self, run_id):
        """Returns a task with this run_id"""
        return self._tasks.get(run_id)

    def set_task(self, run_id, task):
        """Set a test for this run_id"""
        self._tasks[run_id] = task

    def stop(self):
        """Stop the task runner"""
        self._is_running = False
        self._queue.put(None)

    def is_empty(self):
        """Check if the queue is empty"""
        return self._queue.empty()

    def add(self, task):
        """Set a RUN_ID to the task and add the task to the queue"""
        task.RUN_ID = str(uuid.uuid4())
        self.set_task(run_id=task.RUN_ID, task=task)
        self._queue.put(task)
        self.set_status(run_id=task.RUN_ID, status=TaskRunner.WAITING)
        return task.RUN_ID

    def get_status(self, run_id):
        """Returns the status of a Task"""
        task = self.get_task(run_id=run_id)
        return task.STATUS

    def set_status(self, run_id, status):
        """Set status of the task"""
        task = self.get_task(run_id=run_id)
        task.STATUS = status

    def get_logger(self, task):
        """Returns a logger for task"""
        return logging.getLogger(task.RUN_ID)

    def run(self):
        """Task runner thread watches the queue and executes all the tasks
        added to the queue"""
        self._is_running = True
        while self._is_running or not self.is_empty():
            task = self._queue.get()
            if task is None:
                continue
            self.set_status(run_id=task.RUN_ID, status=TaskRunner.RUNNING)
            try:
                task.run(logger=self.get_logger(task=task))
            except Exception as e:
                self.set_status(run_id=task.RUN_ID, status=TaskRunner.ERROR)
                continue
            self.set_status(run_id=task.RUN_ID, status=TaskRunner.COMPLETED)
