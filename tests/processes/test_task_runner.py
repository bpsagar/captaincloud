import unittest
import time
from captaincloud.processes.container import TaskRunner
from captaincloud.task import Task, TaskImpl, field
from captaincloud.task.registry import TaskRegistry


class TestTaskRunner(unittest.TestCase):
    """Test task runner"""

    def setUp(self):
        self.task_runner = TaskRunner()

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

        self.task = AddTask(x=10, y=20)

    def test_add_task(self):
        self.assertTrue(self.task_runner.is_empty())
        run_id = self.task_runner.add(self.task)
        self.assertTrue(hasattr(self.task, 'RUN_ID'))
        self.assertEqual(self.task.RUN_ID, run_id)
        self.assertEqual(
            self.task_runner.get_status(task=self.task),
            TaskRunner.WAITING)
        self.assertFalse(self.task_runner.is_empty())
        self.task_runner.stop()

    def test_task_status(self):
        self.task_runner.add(self.task)
        self.task_runner.set_status(task=self.task, status=TaskRunner.RUNNING)
        self.assertEqual(
            self.task_runner.get_status(task=self.task), TaskRunner.RUNNING)

    def test_task_runner(self):
        self.task_runner.start()
        self.task_runner.add(self.task)
        self.assertTrue(self.task_runner._is_running)
        while not self.task_runner.is_empty():
            time.sleep(1)
        self.task_runner.stop()
        self.assertFalse(self.task_runner._is_running)
        self.assertEqual(
            self.task_runner.get_status(task=self.task), TaskRunner.COMPLETED)
        self.assertTrue(self.task.Output.ans, 30)
