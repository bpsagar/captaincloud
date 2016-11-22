import threading
from captaincloud.task import Task
from captaincloud.utils.http import api


class TaskRunnerAPI(object):
    """Container API using bottle"""

    def __init__(self, process, runner):
        self.process = process
        self.runner = runner

    @api.register
    def submit(self, task):
        """API to accept a serialized task and add it to task runner queue.
        Returns the run_id of the task"""
        task = Task.deserialize(data=task)
        run_id = self.runner.add(task=task)
        return {'run_id': run_id}

    @api.register
    def status(self, run_id):
        """API to check the status of the task"""
        return {'status': self.runner.get_status(run_id=run_id)}

    @api.register
    def stop(self):
        """API to stop the process"""
        thread = threading.Thread(target=self.process.stop)
        thread.start()
        return {}
