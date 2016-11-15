import json
import unittest
from webtest import TestApp
from captaincloud.processes.container.create_api_app import create_api_app
from captaincloud.task import Task, TaskImpl, field
from captaincloud.task.registry import TaskRegistry
from captaincloud.processes.container.task_runner import TaskRunner


class TestContainerAPI(unittest.TestCase):
    """Tests for Container"""

    def setUp(self):
        self.task_runner = TaskRunner()
        self.app = create_api_app(task_runner=self.task_runner)
        self.test_app = TestApp(self.app)

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

    def test_api(self):
        task = self.AddTask(x=10, y=20)
        response = self.test_app.post(
            '/api/submit/', {'task': json.dumps(task.serialize())})
        run_id = response.json.get('run_id')
        self.assertTrue(run_id is not None)

        response = self.test_app.post('/api/status/', {'run_id': run_id})
        self.assertEqual(response.json['task_status'], TaskRunner.WAITING)

        self.task_runner.start()
        self.task_runner.stop()
        self.task_runner.join()

        response = self.test_app.post('/api/status/', {'run_id': run_id})
        self.assertEqual(response.json['task_status'], TaskRunner.COMPLETED)
