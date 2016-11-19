import unittest
from captaincloud.task import Task
from captaincloud.task import field
from captaincloud.task.registry import TaskRegistry
from captaincloud.workflow import Workflow


class TestWorkflow(unittest.TestCase):
    def setUp(self):
        @TaskRegistry.register
        class SleepTask(Task):
            ID = 'sleep'

            class Input:
                duration = field.IntegerField(default=1)

            class Output:
                random = field.IntegerField()

    def test_basics(self):
        t1 = TaskRegistry.create('sleep')
        t2 = TaskRegistry.create('sleep')

        workflow = Workflow()
        workflow.add_task('sleep1', t1)
        workflow.add_task('sleep2', t2)

        with self.assertRaises(Exception):
            workflow.add_task('something', 100)

        self.assertEqual(workflow.get_task('sleep1'), t1)
        self.assertEqual(workflow.pop_task('sleep2'), t2)

        with self.assertRaises(Exception):
            workflow.get_task('sleep2')

        with self.assertRaises(Exception):
            workflow.pop_task('sleep2')

    def test_links(self):
        t1 = TaskRegistry.create('sleep')
        t2 = TaskRegistry.create('sleep')

        workflow = Workflow()
        workflow.add_task('sleep1', t1)
        workflow.add_task('sleep2', t2)

        with self.assertRaises(Exception):
            workflow.connect('sleep1', 'random', 'sleep3', 'duration')

        with self.assertRaises(Exception):
            workflow.connect('sleep1', 'random1', 'sleep2', 'duration')

        with self.assertRaises(Exception):
            workflow.connect('sleep1', 'random', 'sleep2', 'duration1')

        workflow.connect('sleep1', 'random', 'sleep2', 'duration')

    def test_dependency(self):
        t1 = TaskRegistry.create('sleep')
        t2 = TaskRegistry.create('sleep')

        workflow = Workflow()
        workflow.add_task('sleep1', t1)
        workflow.add_task('sleep2', t2)

        workflow.connect('sleep1', 'random', 'sleep2', 'duration')
        self.assertIn((t2, t1), workflow.dependencies)

        with self.assertRaises(Exception):
            workflow.add_dependency('sleep2', 'sleep3')
