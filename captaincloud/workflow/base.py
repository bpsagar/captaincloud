from captaincloud.task import Task


class Workflow(object):
    def __init__(self):
        self.tasks = {}
        self.links = set()
        self.dependencies = set()

    def add_task(self, name, task):
        """Add task to the workflow"""
        if not isinstance(task, Task):
            raise Exception('Not a task')

        self.tasks[name] = task

    def pop_task(self, name):
        """Pop and return task from the workflow"""
        if name not in self.tasks:
            raise Exception('Task not found')
        return self.tasks.pop(name)

    def get_task(self, name):
        """Get the task by name"""
        if name not in self.tasks:
            raise Exception('Task not found')
        return self.tasks.get(name)

    def connect(self, task1, task1_output, task2, task2_input):
        """Connect input and output of tasks"""
        if task1 not in self.tasks or task2 not in self.tasks:
            raise Exception('Task not found')

        t1 = self.get_task(task1)
        t2 = self.get_task(task2)

        if not hasattr(t1.Output, task1_output):
            raise Exception('Invalid output property')

        if not hasattr(t2.Input, task2_input):
            raise Exception('Invalid input property')

        self.links.add((t1, task1_output, t2, task2_input))
        self.add_dependency(task2, task1)

    def add_dependency(self, depending_task, depended_task):
        """Add dependency of two tasks"""
        if depending_task not in self.tasks or depended_task not in self.tasks:
            raise Exception('Task not found')

        depending_task = self.get_task(depending_task)
        depended_task = self.get_task(depended_task)

        self.dependencies.add((depending_task, depended_task))
