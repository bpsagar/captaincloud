import base64
import pickle
import six
import unittest

from captaincloud.task.field import InvalidValueException
from captaincloud.task import field
from captaincloud.task import Task
from captaincloud.task.registry import TaskRegistry


class TestFields(unittest.TestCase):
    """Tests for tasks"""

    def setUp(self):
        @TaskRegistry.register
        class RandomTask(Task):
            ID = 'random'
            NAME = 'Random'

            class Input:
                string = field.StringField(default=six.u('ABCD'))
                integer = field.IntegerField(default=5)
                instream = field.StringStreamField()
                integer_array = field.ListField(field.IntegerField())
                anyf = field.AnyField(default={1: 2})

            class Output:
                floating = field.FloatField(default=1.5)
                none = field.IntegerField()
                outstream = field.ByteStreamField()

        self.RandomTask = RandomTask

    def test_task_init(self):
        task = self.RandomTask(string=six.u('XYZ'), integer=10)
        self.assertEqual(task.Input.string, six.u('XYZ'))
        self.assertEqual(task.Input.integer, 10)

        task.set_input(string=six.u('DEF'), integer=20)
        self.assertEqual(task.Input.string, six.u('DEF'))
        self.assertEqual(task.Input.integer, 20)

    def test_task_fields(self):
        task = self.RandomTask()

        self.assertEqual(task.Input.string, six.u('ABCD'))
        task.Input.string = six.u('XYZ')
        self.assertEqual(task.Input.string, six.u('XYZ'))
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

        task2 = self.RandomTask()
        self.assertEqual(task2.Input.string, 'ABCD')
        task2.Input.string = six.u('123')
        self.assertEqual(task2.Input.string, six.u('123'))

        # Test if the tasks share the same fields
        self.assertEqual(task.Input.string, six.u('XYZ'))

        # Check if it's cloned
        self.assertNotEqual(task.Input.instream, task2.Input.instream)

    def test_task_serialize(self):
        task = self.RandomTask()
        serialized = {
            'ID': 'random',
            'Input': {
                'string': six.u('ABCD'),
                'integer': 5,
                'integer_array': [],
                'anyf': six.u(base64.b64encode(pickle.dumps({1: 2})))
            },
            'Output': {
                'floating': 1.5,
                'none': None
            }
        }
        self.assertEqual(task.serialize(), serialized)

        task = self.RandomTask()
        task.Input.string = six.u('XYZ')
        task.Input.integer = 10
        task.Input.integer_array = [1, 2, 3]
        task.Input.anyf = ['hello', 'world']
        task.Output.floating = 2.5
        serialized = {
            'ID': 'random',
            'Input': {
                'string': six.u('XYZ'),
                'integer': 10,
                'integer_array': [1, 2, 3],
                'anyf': six.u(base64.b64encode(pickle.dumps(['hello', 'world'])))
            },
            'Output': {
                'floating': 2.5,
                'none': None
            }
        }
        self.assertEqual(task.serialize(), serialized)

    def test_task_deserialize(self):
        serialized = {
            'ID': 'random',
            'Input': {
                'string': six.u('ABCD'),
                'integer': 5,
                'integer_array': [1, 2, 3],
                'anyf': six.u(base64.b64encode(pickle.dumps(100)))
            },
            'Output': {
                'floating': 1.5,
                'none': None
            }
        }
        instance = Task.deserialize(data=serialized)
        self.assertTrue(isinstance(instance, self.RandomTask))
        self.assertEqual(instance.Input.string, six.u('ABCD'))
        self.assertEqual(instance.Input.integer, 5)
        self.assertEqual(instance.Output.floating, 1.5)

        serialized = {
            'ID': 'random',
            'Input': {
                'string': six.u('XYZ'),
                'integer': 10
            },
            'Output': {
                'floating': 2.5,
                'none': None
            }
        }
        instance = Task.deserialize(data=serialized)
        self.assertTrue(isinstance(instance, self.RandomTask))
        self.assertEqual(instance.Input.string, six.u('XYZ'))
        self.assertEqual(instance.Input.integer, 10)
        self.assertEqual(instance.Output.floating, 2.5)
