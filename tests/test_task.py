import unittest
from captaincloud.task.field import InvalidValueException
from captaincloud.task import field
from captaincloud.task import Task
from captaincloud.task.registry import TaskRegistry


class TestFields(unittest.TestCase):
    """Tests for tasks"""

    def test_task(self):

        @TaskRegistry.register
        class RandomTask(Task):
            ID = 'random'
            NAME = 'Random'

            class Input:
                string = field.StringField(default='ABCD')
                integer = field.IntegerField(default=5)

            class Output:
                floating = field.FloatField(default=1.5)

        task = RandomTask()

        self.assertEqual(task.Input.string, 'ABCD')
        task.Input.string = 'XYZ'
        self.assertEqual(task.Input.string, 'XYZ')
        with self.assertRaises(InvalidValueException):
            task.Input.string = 10

        self.assertEqual(task.Input.integer, 5)
        task.Input.integer = 10
        self.assertEqual(task.Input.integer, 10)
        with self.assertRaises(InvalidValueException):
            task.Input.integer = 'ABCD'

        self.assertEqual(task.Output.floating, 1.5)
        task.Output.floating = 5.5
        self.assertEqual(task.Output.floating, 5.5)
        with self.assertRaises(InvalidValueException):
            task.Output.floating = 'ABCD'
