import unittest
from captaincloud.task.registry import TaskRegistry


class TestTaskRegistry(unittest.TestCase):
    """Tests for Task Registry"""

    def test_register(self):
        """Test the register class method"""

        @TaskRegistry.register
        class DummyTask(object):
            ID = 'dummy'

        self.assertIn(DummyTask, TaskRegistry.all())
        self.assertEqual(TaskRegistry.get(id='dummy'), DummyTask)
        self.assertIsInstance(TaskRegistry.create(id='dummy'), DummyTask)
