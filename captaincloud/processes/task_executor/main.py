from captaincloud.engine.executor import TaskExecutor, TaskExecutorStatus

import argparse
import importlib


def load_modules(modules):
    for module in modules:
        if module == '':
            continue
        try:
            importlib.import_module(module)
        except ImportError:
            raise Exception('Failed to load the module.')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', default='stdin', help='Task file')
    parser.add_argument('--task-out', default='stdout',
                        help='Task output after execution')
    parser.add_argument('--modules', default='',
                        help='Modules to load to register necessary tasks')
    return parser.parse_args()


def main():
    args = parse_args()

    load_modules(args.modules.split(','))

    executor = TaskExecutor()
    executor.load_task(args.task)

    executor.execute()

    if executor.status == TaskExecutorStatus.SUCCESS:
        executor.dump_task(args.task_out)


if __name__ == '__main__':
    main()
