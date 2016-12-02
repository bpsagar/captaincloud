from captaincloud.engine.executor import TaskExecutor
from captaincloud.task import Task, TaskImpl
from captaincloud.task.registry import TaskRegistry

from captaincloud.task import field

import os
import six
import unittest


class AddTaskImpl(TaskImpl):
    def run(self):
        Input = self.task.Input
        Output = self.task.Output
        Output.c = Input.a + Input.b


@TaskRegistry.register
class AddTask(Task):
    ID = 'test_executor_add'
    impl = AddTaskImpl

    class Input:
        a = field.IntegerField(default=0)
        b = field.IntegerField(default=0)

    class Output:
        c = field.IntegerField()


class StreamCopyImpl(TaskImpl):
    def run(self):
        Input = self.task.Input
        Output = self.task.Output

        data = Input.stream.read(10)
        while len(data) > 0:
            Output.stream.write(data)
            data = Input.stream.read(10)
        Input.stream.close()
        Output.stream.close()


@TaskRegistry.register
class StreamCopy(Task):
    ID = 'test_executor_stream_copy'
    impl = StreamCopyImpl

    class Input:
        stream = field.ByteStreamField()

    class Output:
        stream = field.ByteStreamField()


class TestTaskExecutor(unittest.TestCase):
    def test_simple(self):
        task1 = TaskRegistry.create('test_executor_add')
        task1.Input.a = 10
        task1.Input.b = 20

        task2 = TaskRegistry.create('test_executor_add')
        task2.Input.a = 100
        task2.Input.b = 200

        executor1 = TaskExecutor(task=task1)
        executor1.execute()

        executor2 = TaskExecutor(task=task2)
        executor2.execute()

        self.assertEqual(task1.Output.c, 30)
        self.assertEqual(task2.Output.c, 300)

    def test_stream(self):
        with open('test.tmp', 'wb') as fd:
            fd.write(six.b('Hello World ') * 100)

        task = TaskRegistry.create('test_executor_stream_copy')
        task.Input.stream = open('test.tmp', 'rb')
        task.Output.stream = open('test.out', 'wb')

        executor = TaskExecutor(task=task)
        executor.execute()

        with open('test.out', 'rb') as fd:
            self.assertEqual(fd.read(), six.b('Hello World ') * 100)

        os.unlink('test.tmp')
        os.unlink('test.out')
