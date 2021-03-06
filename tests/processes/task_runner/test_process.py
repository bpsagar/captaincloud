import json
import requests
import threading
import unittest
from captaincloud.task import Task, TaskImpl, field
from captaincloud.task.registry import TaskRegistry

from captaincloud.processes.task_runner import TaskRunner
from captaincloud.processes.task_runner import TaskRunnerProcess


class TestTaskRunnerProcess(unittest.TestCase):
    """Tests for Container"""

    def setUp(self):
        self.container = TaskRunnerProcess(host='localhost', port=10000)

        class AddTaskImpl(TaskImpl):
            def run(self):
                self.task.Output.ans = self.task.Input.x + self.task.Input.y

        @TaskRegistry.register
        class AddTask(Task):
            ID = 'add'
            impl = AddTaskImpl

            class Input:
                x = field.FloatField()
                y = field.FloatField()

            class Output:
                ans = field.FloatField()

        self.AddTask = AddTask

    def test_container(self):
        process = threading.Thread(target=self.container.run)
        process.start()

        task = self.AddTask(x=10, y=20)
        response = requests.post(
            'http://localhost:10000/api/submit/',
            {'data': json.dumps({'task': task.serialize()})})
        run_id = response.json().get('data', {}).get('run_id')
        self.assertTrue(run_id is not None)

        response = requests.post(
            'http://localhost:10000/api/status/',
            {'data': json.dumps({'run_id': run_id})})
        self.assertEqual(
            response.json().get('data', {}).get('status'),
            TaskRunner.COMPLETED)

        response = requests.post(
            'http://localhost:10000/api/stop/', {'data': json.dumps({})})
        self.assertEqual(response.json().get('data', {}), {})

        process.join()
