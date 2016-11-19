import threading
from captaincloud.task import Task
from captaincloud.utils import bottle_utils


class ContainerAPI(object):
    """Container API using bottle"""

    def __init__(self, container):
        self.container = container

    @bottle_utils.register_api
    def submit(self, task):
        """API to accept a serialized task and add it to task runner queue.
        Returns the run_id of the task"""
        task = Task.deserialize(data=task)
        run_id = self.container.task_runner.add(task=task)
        return {'run_id': run_id}

    @bottle_utils.register_api
    def status(self, run_id):
        """API to check the status of the task"""
        return {'status': self.container.task_runner.get_status(run_id=run_id)}

    @bottle_utils.register_api
    def stop(self):
        """API to stop the container"""
        thread = threading.Thread(target=self.container.stop)
        thread.start()
        return {}
