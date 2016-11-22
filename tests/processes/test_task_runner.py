import unittest
from captaincloud.processes.task_runner import TaskRunner

from captaincloud.task import Task, TaskImpl, field
from captaincloud.task.registry import TaskRegistry


class TestTaskRunner(unittest.TestCase):
    """Test task runner"""

    def setUp(self):
        self.task_runner = TaskRunner()

        class DivideTaskImpl(TaskImpl):
            def run(self):
                self.task.Output.ans = self.task.Input.x / self.task.Input.y

        @TaskRegistry.register
        class DivideTask(Task):
            ID = 'add'
            impl = DivideTaskImpl

            class Input:
                x = field.FloatField()
                y = field.FloatField()

            class Output:
                ans = field.FloatField()

        self.task = DivideTask(x=20, y=2)
        self.error_task = DivideTask(x=20, y=0)

    def test_add_task(self):
        self.assertTrue(self.task_runner.is_empty())
        run_id = self.task_runner.add(self.task)
        self.assertTrue(hasattr(self.task, 'RUN_ID'))
        self.assertEqual(self.task.RUN_ID, run_id)
        self.assertEqual(
            self.task_runner.get_status(run_id=run_id),
            TaskRunner.WAITING)
        self.assertFalse(self.task_runner.is_empty())
        self.task_runner.stop()

    def test_task_status(self):
        run_id = self.task_runner.add(self.task)
        self.task_runner.set_status(run_id=run_id, status=TaskRunner.RUNNING)
        self.assertEqual(
            self.task_runner.get_status(run_id=run_id), TaskRunner.RUNNING)

    def test_task_runner(self):
        self.task_runner.start()
        self.assertTrue(self.task_runner._is_running)
        run_id1 = self.task_runner.add(self.task)
        run_id2 = self.task_runner.add(self.error_task)
        self.assertTrue(self.task_runner._is_running)
        self.task_runner.stop()
        self.task_runner.join()

        self.assertFalse(self.task_runner._is_running)
        self.assertEqual(
            self.task_runner.get_status(run_id=run_id1), TaskRunner.COMPLETED)
        self.assertTrue(self.task.Output.ans, 30)

        self.assertEqual(self.task_runner.get_status(
            run_id=run_id2), TaskRunner.ERROR)
