import threading
import uuid
from six.moves import queue


class TaskRunner(threading.Thread):
    """Class that has a task queue and runs the tasks one by one"""
    WAITING = 'WAITING'
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'

    def __init__(self, *args, **kwargs):
        super(TaskRunner, self).__init__(*args, **kwargs)
        self._queue = queue.Queue()
        self._is_running = False

    def stop(self):
        """Stop the task runner"""
        self._is_running = False

    def is_empty(self):
        """Check if the queue is empty"""
        return self._queue.empty()

    def add(self, task):
        """Set a RUN_ID to the task and add the task to the queue"""
        task.RUN_ID = str(uuid.uuid4())
        self.set_status(task=task, status=TaskRunner.WAITING)
        self._queue.put(task)
        return task.RUN_ID

    def get_status(self, task):
        """Returns the status of a Task"""
        return task.STATUS

    def set_status(self, task, status):
        """Set status of the task"""
        task.STATUS = status

    def run(self):
        """Task runner thread watches the queue and executes all the tasks
        added to the queue"""
        self._is_running = True
        while self._is_running or not self.is_empty():
            try:
                task = self._queue.get(block=True, timeout=1)
            except queue.Empty:
                continue
            self.set_status(task=task, status=TaskRunner.RUNNING)
            task.run()
            self.set_status(task=task, status=TaskRunner.COMPLETED)
