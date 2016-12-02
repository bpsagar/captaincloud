from captaincloud.task import Task

from captaincloud.engine.executor import TaskExecutor, TaskExecutorStatus

import argparse
import importlib
import json
import sys


def load_modules(modules):
    for module in modules:
        if module == '':
            continue
        try:
            importlib.import_module(module)
        except ImportError:
            print('Failed to load the module.')
            sys.exit(-1)


def load_task(task_in):
    if task_in == 'stdin':
        fd = sys.stdin
    else:
        fd = open(task_in, 'r')
    try:
        task_data = json.load(fd)
    except json.decoder.JSONDecodeError:
        print('Unable to load task data.')
        sys.exit(-1)
    fd.close()
    task = Task.deserialize(task_data)
    return task


def dump_task(task, task_out):
    if task_out == 'stdout':
        fd = sys.stdout
    else:
        fd = open(task_out, 'w')
    json.dump(task.serialize(), fd)
    fd.close()


def create_executor(task):
    return TaskExecutor(task=task)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', default='stdin', help='Task file')
    parser.add_argument('--task-out', default='stdout',
                        help='Task output after execution')
    parser.add_argument('--modules', default='',
                        help='Modules to load to register necessary tasks')
    args = parser.parse_args()

    load_modules(args.modules.split(','))
    task = load_task(args.task)
    executor = create_executor(task=task)

    executor.execute()

    if executor.status == TaskExecutorStatus.SUCCESS:
        dump_task(task, args.task_out)


if __name__ == '__main__':
    main()
