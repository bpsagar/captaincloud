import unittest
from captaincloud.task import Task, TaskImpl, field
from captaincloud.task.registry import TaskRegistry


class TestTaskImpl(unittest.TestCase):
    """Tests for Task and TaskImpl"""

    def test_task_impl_no_run_implementation(self):

        class DummyTaskImpl(TaskImpl):
            pass

        @TaskRegistry.register
        class DummyTask(Task):
            ID = 'dummy'
            impl = DummyTaskImpl

        task = DummyTask()
        with self.assertRaises(NotImplementedError):
            task.run()

    def test_task_impl(self):

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

        task = AddTask()
        task.Input.x = 10
        task.Input.y = 20
        task.run()
        self.assertEqual(task.Output.ans, 30)
